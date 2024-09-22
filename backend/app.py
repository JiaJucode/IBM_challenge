## Flask APIs. Return JSON data
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from database import ChatsDatabase
import utils.ai as bot
import utils.google_search_client as google_search
from utils.language_model import sentence_similarity

app = Flask(__name__)
chat_db = ChatsDatabase()

def get_ai_response(message, cache_num=0) -> tuple[str, list]:
    search_query = bot.process_search_query(message)
    similar_searches = []

    if cache_num:
        history = chat_db.get_searches()
        similarity_scores = sentence_similarity(search_query, [entry["search_term"] for entry in history])
        for i in range(len(history)):
            if len(similar_searches) > cache_num:
                break
            if similarity_scores[i] > 0.9 and len(similar_searches):
                similar_searches.append(history[i])

    if similar_searches:
        website_contents = google_search.extract_content(search_query)
        return bot.summarize_search_results(search_query, website_contents), []
    else:
        return f"I found {len(similar_searches)} similar searches in the history matching your requirement.\
              Click on the search terms to view previous seaches or perform new search on: {search_query}", similar_searches
     
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
    uid = 0
    chats = chat_db.get_chats(uid)
    return jsonify({'chats': chats})

@app.route('/api/start', methods=['POST'])
def create_chat():
    '''
    Request format:
    {
        'initial_message': <message>
    }

    Response format:
    {
        'chat_id': <chat_id>
        'title': <chat_title>,
        'response': <response>
    }
    '''
    # get chat title
    initial_message = request.get_json()['initial_message']
    chat_title = bot.create_chat_title(initial_message)

    # create chat in Chats table
    user_id = 0
    chat_id = chat_db.create_chat(user_id, chat_title)

    # add initial message to Messages table
    chat_db.add_message(chat_id, 'user', initial_message)
    
    # get search response
    response, cache = get_ai_response(initial_message)
    chat_db.add_message(chat_id, 'assistant', response)
    return jsonify({'chat_id': chat_id, 'title': chat_title, 'response': response, 'cache': cache})



@app.route('/api/chat', methods=['GET'])
def load_chat():
    '''
    Get a chat and its messages by chat ID. If the most recent message is 'user', add to request 
        'add_query=false' and 'message=<most recent message>'

    Request format:
    {
        'chat_id': <chat_id>,
    }
    Return format:
    {
        'messages': [
            {
                'role': <role>,
                'content': <content>
            }
        ]
    }
    '''
    chat_id = request.args.get('chat_id')
    print("chat_id: ", chat_id)
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
    }

    Response format:
    {
        'response': <response>
    }
    '''

    # Get required parameters from request
    request_data = request.get_json()
    chat_id = request_data.get('chat_id')
    message = request_data.get('message')
    chat_db.add_message(chat_id, 'user', message)

    # Get AI response
    response, cache = get_ai_response(message)
    chat_db.add_message(chat_id, 'assistant', response)

    return jsonify({'response': response, 'cache': cache})



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)