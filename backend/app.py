## Flask APIs. Return JSON data
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

# Enable CORS for requests only to /api/* from frontend server
CORS(app, resources={r"/api/*": {"origins": "http://localhost:3000"}})

@app.route('/api/hello', methods=['GET'])
def hello():
    return jsonify({'message': 'Hello World!'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)