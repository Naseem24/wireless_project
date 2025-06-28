# backend/app.py
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from the .env file
load_dotenv()

# Initialize the Flask app
app = Flask(__name__)

# --- CONFIGURATION ---
# Enable Cross-Origin Resource Sharing (CORS)
CORS(app) 
# Initialize the OpenAI client with the API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# --- API ENDPOINTS ---
@app.route("/api/test")
def test_endpoint():
    """A simple test endpoint to check if the backend is running."""
    # We will add a simple AI call here just to test the key
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Say 'AI connection is successful.'"}
            ],
            max_tokens=15
        )
        ai_message = completion.choices[0].message.content
        return jsonify({
            "backend_status": "Backend is running and connected!",
            "ai_status": ai_message
            })
    except Exception as e:
        # If the API key is invalid or there's an issue, we'll see it here
        return jsonify({"error": f"AI connection failed: {str(e)}"}), 500