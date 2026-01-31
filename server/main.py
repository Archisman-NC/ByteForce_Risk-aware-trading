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

{
    "response": "Hello! I'm your AI stock analysis assistant. Please tell me which stock you'd like to analyze today. \n"
}
{
    "response": [
        {
            "extras": {
                "signature": "CmQBcsjafO4Z7+wRqWa/PtH0Cmbh3nFkdyVFujHUi1TBr27FsCmGnTgHkRVilCBSFCJVNuhf3EQdOUQMTAwxERYCH/2+DDPJxTVYYX60jhNqdRGPgWXbbTQvb87zJ1m+x9ZTD5mFCr8BAXLI2nw0bqsRkj3ZpStDBsFWOcly68V8eWCUYC176u1lD7NsPY5kVSl5oKqCJq++2F4APywhkBL6M3zOTb6YJffHiuqVLNCeLHD6FPVYmZ1N+lBb4DeJ7TevLccpzPHOmqRABARSRP2d/4s4u/scL1NCYqAIx7jsx8WeMxuDF8QYNUhYXle37n5a7XQFOICb+LJVxl5Maun6pO4DXpAut7oleZcwQh3E8e/JjDBrrAusE6yNW0SFvOqHnAMMuoYK0AEBcsjafJ4sIGmK6995zm8Uqk3svdJMtgHmLreEG9F0Cx3UlqzoWXGGooG700tPEsN86px1LSyf6lgpwaf43lxzkB1USnCpw2saAsrpxkfMSQZ3tvE58pzindg5yorCcjknViSR3E5BLTloRcc9VUw3e6W8xUsfpnMxbits1aqagsAnhCK1myAJBxLCOZytAU/pN4DfOm8FH81TMA1JeoS4AzhTkcjIeVuixKqCY0cXRy8Puh+Z+LTpcd79HbaiCZ6rZZ8jy7JCM9cwBkkvxu1KClYBcsjafDUgRQLyQJMRw1zf04g+hiBCqS3PBWKjcZ56mg/c57nkogDHAs3IArLOBDd8Qi698EyYQSfPeprbH3SIXVd/3U+oyV4ptVUks1TbxPjyPmAmbg=="
            },
            "index": 0,
            "text": "Given the current VOLATILE market regime and HIGH risk level, the recommendation for Amazon stock is to **HOLD** with a confidence level of 7",
            "type": "text"
        },
        "9%. This is due to elevated volatility and high agent disagreement."
    ]
}