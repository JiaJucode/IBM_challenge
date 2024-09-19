## Flask APIs. Return JSON data
from flask import Flask, jsonify, request
from flask_cors import CORS
from database import ChatsDatabase, SearchResponseDatabase
import json

app = Flask(__name__)
chat_db = ChatsDatabase()
search_db = SearchResponseDatabase()

def get_ai_response(message):
    return "I am a bot"

# Enable CORS for requests only to /api/* from frontend server
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})


@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello World!'})


@app.route('/api/chat/<int:chat_id>', methods=['GET'])
def get_chat(chat_id):
    '''
    Get a chat and its messages by chat ID.

    Return format:
    {
        'chat': {
            'id': <chat_id>,
            'search_query': <search_query>,
            'summarized_search_results': <summarized_search_results>
        },
        'messages': [
            {
                'role': <role>,
                'content': <content>,
                'timestamp': <timestamp>
            },
            ...
        ]
    '''
    chat = chat_db.get_chat(chat_id)
    return jsonify(chat)


@app.route('/api/chats', methods=['GET'])
def get_chats():
    '''
    Get high level info for all chats.

    Return format:
        [
            {
                'id': <chat_id>,
                'search_query': <search_query>,
                'summarized_search_results': <summarized_search_results>
            },
            ...
        ]
    '''
    chats = chat_db.get_chats()
    return jsonify(chats)


@app.route('/api/ai_response', methods=['POST'])
def get_ai_response():
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

    # Attempt to get AI response
    try:
        response = get_ai_response(message)
    except Exception as e:
        return jsonify({'error': f"Error getting AI response: {e}"}), 500
    
    # Save messages
    chat_db.add_message(chat_id=chat_id, role='user', content=message)
    chat_db.add_message(chat_id=chat_id, role='assistant', content=response)

    return jsonify({'response': response})
    
# On closing the app
@app.teardown_appcontext
def close_connection(exception):
    chat_db.close()
    search_db.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)