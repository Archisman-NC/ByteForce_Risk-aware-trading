from flask import Flask, jsonify, request
from chat_bot import chat

app = Flask(__name__)

@app.route('/')
def home():
  return jsonify({"message": "Welcome to Flask Server"})

@app.route('/api/health', methods=['GET'])
def health():
  return jsonify({"status": "healthy"}), 200

@app.route('/api/chat', methods=['POST'])
def chat_api():
  data = request.get_json()
  user_question = data.get('question')
  if not user_question:
    return jsonify({"error": "Missing 'question' in request body"}), 400
  response = chat(user_question)
  return jsonify(response), 200

if __name__ == '__main__':
  app.run(debug=True, port=5000)