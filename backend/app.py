## Flask APIs. Return JSON data
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from database import ChatsDatabase
import utils.ai as bot
from utils.google_maps_places import MapsTextSearch
import json

app = Flask(__name__)
chat_db = ChatsDatabase()

def get_ai_response(message):
    return "I am a bot"

# Enable CORS for requests only to /api/* from frontend server
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


@app.route('/api/hello', methods=['GET'])
def hello():
    '''Welcome page showing recent chats and include a text box (form input) to begin a chat
    Return format:
    {
        'chats': [
            {
                'id': <chat_id>,
                'title': <chat_title>
            }
        ],
    }
    '''
    chats = chat_db.recent_chats()
    return jsonify(chats)

@app.route('/api/start', methods=['GET'])
def create_chat():
    '''
     Request format:
    {
        'initial_message': <message>
    }
    '''
    inimesg = request.form.get("initial_message")
    title = inimesg
    # Summarize user initial query if it's longer than 200 characters
    if len(title) > 200:
        title = bot.create_chat_title(title)
    
    # Prompt user with similar chats if the new title is close enough to some existing ones
    if similar := chat_db.similar_chats(title):
        '''
            Return format:
            [
                {
                    'id': <chat_id>,
                    'title': <chat_title>,
                    'similarity': <n% similar>
                    'search_list': [
                        {
                            'id': <search_id>
                            'search_term': <search_term>
                            'mode': <Google search | Google maps>
                        }
                        ...
                    ]
                },
                ...
            ]
        '''
        return jsonify(similar)
    # Otherwise, create a new chat and redirect to the chat page with user's initial message
    else:
        new_id = chat_db.create_chat(title)
        chat_db.add_message(new_id, 'user', inimesg)
        return redirect(f'/api/chat/{new_id}')

@app.route('/api/chat/<int:chat_id>', methods=['GET'])
def load_chat(chat_id):
    '''
    Get a chat and its messages by chat ID. If the most recent message is 'user', add to request 
        'add_query=false' and 'message=<most recent message>'
    Return format:
    {
        'chat': {
            'id': <chat_id>,
            'title': <chat_title>,
        },
        'messages': [
            {
                'role': <role>,
                'content': <content>,
                'timestamp': <timestamp>
            },
            ...
        ]
        'searches': [
            {
                'id': <seach_id>,
                'search_term': <term>,
                'mode': <Google maps | Google search>
            },
            ...
        ]
    '''
    chat = chat_db.get_chat(chat_id)
    return jsonify(chat)

@app.route('/api/ai_response', methods=['POST'])
def get_response():
    '''
    Gets response for user message from AI, and adds both new messages to the chat history.

    Request format:
    {
        'chat_id': <chat_id>,
        'message': <message>
        'add_query': <true | false>
        'mode': <Google search | Google maps>
    }
    '''

    # Get required parameters from request
    request_data = request.get_json()
    chat_id = request_data.get('chat_id')
    message = request_data.get('message')
    mode = request_data.get('mode')

    # Attempt to get AI response
    try:
        search_terms = bot.process_search_query(message)
        response = ""
        if sim_searches := chat_db.similar_searches(search_terms, mode):
            response = "I found some of the previous searches similar to your requirement:"
            for search in sim_searches:
                chat_db.add_search(id=search["id"])
                response += f"\n<{search["search_term"]}> ({100*search["similarity"]}% similar)\n{search["summarized_response"]}"
            chat_db.chat_add_search(chat_id,[str(search["id"]) for search in sim_searches])
        elif mode == "Google maps":
            maps_tool = MapsTextSearch()
            all_places = []
            for term in search_terms.split(";"):
                # Perform maps search on each individual search term element
                maps_tool.query = term
                places = json.dumps(maps_tool.get_response())
                all_places.append(places)

            # TODO Search places on Google maps and summarize response
            chat_db.add_search(search_terms, mode, response)

        elif mode == "Google search":
            # TODO Search Google and summarize response
            chat_db.add_search(search_terms, mode, response)

        response = get_ai_response(message)
    except Exception as e:
        return jsonify({'error': f"Error getting AI response: {e}"}), 500
    
    # Save messages to database and redirect to chat page
    if request_data.get('add_query') == "true":
        chat_db.add_message(chat_id=chat_id, role='user', content=message)
    chat_db.add_message(chat_id=chat_id, role='assistant', content=response)

    return redirect(f'/api/chat/{chat_id}')
    
@app.route('/api/chats', methods=['GET'])
def get_chats():
    '''
    Get high level info for all chats, including AI generated search terms contained

    Return format:
        [
            {
                'id': <chat_id>,
                'title': <chat_title>,
                'search_list': [
                    {
                        'id': <search_id>
                        'search_term': <search_term>
                        'mode': <Google search | Google maps>
                    }
                    ...
                ]
            },
            ...
        ]
    '''
    chats = chat_db.get_chats()
    return jsonify(chats)

# On closing the app
@app.teardown_appcontext
def close_connection(exception):
    chat_db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)