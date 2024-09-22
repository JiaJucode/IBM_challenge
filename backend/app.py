## Flask APIs. Return JSON data
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS
from database import ChatsDatabase
import utils.ai as bot
import utils.google_search_client as google_search
from utils.helpers import get_middle_truncated_text

app = Flask(__name__)
chat_db = ChatsDatabase()

def get_ai_response(message):
    search_query = bot.process_search_query(message)
    website_contents = google_search.scrape_contents(search_query)
    return bot.summarize_search_results(search_query, website_contents)

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
        'search_query': <message>
    }

    Response format:
    {
        'chat_id': <chat_id>
        'title': <chat_title>,
        'response': <response>
    }
    '''
    
    search_query = request.get_json()['search_query']

    # perform search
    search_results = google_search.search(search_query, top_n=3)

    # scrape contents of each search result website
    scraped_contents = google_search.scrape_contents([search_result["link"] for search_result in search_results])
    for i, scraped_content in enumerate(scraped_contents):
        search_results[i]["content"] = get_middle_truncated_text(scraped_content)

    # generate summary for each search result
    for i, search_result in enumerate(search_results):
        search_result["summary"] = bot.summarize_result_website(search_query, search_result["content"])

    # summarize overall search results
    search_summary = bot.summarize_search_results(search_query, search_results)

    # create chat for the search
    user_id = 0  # no user auth yet
    chat_id = chat_db.create_chat(uid=user_id, search_query=search_query, search_summary=search_summary)
    
    return jsonify({'chat_id': chat_id, 'title': search_query, 'response': search_summary})


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
        'message': <message>,
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

    chat = chat_db.get_chat(chat_id)
    search_query = chat['title']
    search_summary = chat['search_summary']
    message_history = chat['messages'][-4:]  # last 2 message pairs
    
    # Get AI response
    # response = get_ai_response(message)
    response = bot.chat(message=message, search_query=search_query, search_summary=search_summary, message_history=message_history)

    # Add new messages to chat history
    chat_db.add_message(chat_id=chat_id, role='user', content=message)
    chat_db.add_message(chat_id=chat_id, role='assistant', content=response)

    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)