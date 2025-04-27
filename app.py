import os
import logging  
from dotenv import load_dotenv
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from subs.client_config import ConfigLlm
from subs.ai_agent import assistant_define, assistant_response_generator

load_dotenv()

app = Flask(__name__)
CORS(app) 

logging.basicConfig(level=logging.DEBUG)  
app.logger.setLevel(logging.DEBUG)


API_HOST = os.getenv("API_HOST", "azure")
client = ConfigLlm(API_HOST=API_HOST)
assistant = assistant_define(client)
conversation_history = {}



@app.route('/')
def index():
    return send_from_directory('./front-end', 'chat_bot.html')

@app.route('/chat', methods=['POST'])
async def chat():  
    data = request.json
    user_message = data.get('message')

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    app.logger.info(f"Received message: {user_message}")

    full_response = "" 
    try:
        async for chunk in assistant.run_stream(task=user_message):
            chunk_text = None
            full_response = await assistant_response_generator(chunk, chunk_text, full_response)
        print() 
        app.logger.info(f"Assistant response generated: {full_response}") 
        return jsonify({"response": full_response})

    except Exception as e:
        app.logger.error(f"Error during chat processing: {e}", exc_info=True) # Add exc_info for detailed traceback
        return jsonify({"error": "An error occurred processing your request"}), 500


@app.route('/clear', methods=['POST'])
def clear_history():
    data = request.json
    session_id = data.get('session_id', 'default_session')
    
    # Clear the conversation history for this session
    if session_id in conversation_history:
        conversation_history[session_id] = []
    
    return jsonify({"status": "success", "message": "Conversation history cleared"})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)


