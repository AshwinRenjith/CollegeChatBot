from flask import Flask, request, jsonify
from flask_cors import CORS
from src.query_processor import QueryProcessor
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Initialize QueryProcessor
# Ensure GEMINI_API_KEY is set in your environment variables or .env file
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY not found in environment variables. Please check your .env file.")

query_processor = QueryProcessor(pdf_path="data/SVPCET Details.pdf", gemini_api_key=gemini_api_key)

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400

    try:
        response = query_processor.process_query(user_message)
        return jsonify({'response': response})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)