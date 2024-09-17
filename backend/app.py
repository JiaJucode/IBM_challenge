## Flask APIs. Return JSON data
from flask import Flask, jsonify, request
from flask_cors import CORS
from session import ChatHistoryDatabase, SearchResponseDatabase
import json

app = Flask(__name__)
chat_db = ChatHistoryDatabase()
search_db = SearchResponseDatabase()

def aiResponse(message):
    return "I am a bot"

# Enable CORS for requests only to /api/* from frontend server
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello World!'})

def get_chat_history(chat_ID):
    chat_history = chat_db.get_chat_history(chat_ID)[0]
    return jsonify({'chat_history': chat_history})

def get_user_chats(user_ID):
    chat = chat_db.get_user_chats(user_ID)
    chat_IDs, chat_names = zip(*chat) if chat else ([], [])
    return jsonify([{'chat_ID': chat_ID, 'chat_name': chat_name} 
                    for chat_ID, chat_name in zip(chat_IDs, chat_names)])

@app.route('/api/ChatHistory', methods=['GET'])
def handle_get_chat_history():
    chat_db.start()
    chat_ID = request.args.get('chat_ID')
    user_ID = request.args.get('user_ID')
    if chat_ID:
        return get_chat_history(chat_ID)
    elif user_ID:
        return get_user_chats(user_ID)
    else:
        return jsonify({'error': 'chat_ID or user_ID parameter is required'})

@app.route('/api/AIResponse', methods=['POST'])
def add_chat_message():
    chat_ID = request.json['chat_ID']
    message = request.json['message']
    chat_db.start()
    chat_db.add_message(chat_ID, message)
    response = aiResponse(message)
    chat_db.add_message(chat_ID, response)
    # not closing the database connection to reduce overhead
    chat_db.save_exit()
    return jsonify({'response': response})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)