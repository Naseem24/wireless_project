# backend/app.py
import os
from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
from openai import OpenAI
from calculations import calculate_wireless_system_logic, calculate_ofdm_logic, calculate_link_budget_logic, calculate_cellular_design_logic
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
    # Add this new endpoint to backend/app.py

@app.route("/api/wireless-system", methods=['POST'])
def handle_wireless_system():
    """Receives data, gets calculation and AI explanation, returns all."""
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    numerical_results = calculate_wireless_system_logic(data)
    if "error" in numerical_results:
        return jsonify(numerical_results), 400

    prompt = f"""
    Act as an expert wireless communications engineer explaining results to a student.

    Scenario: Wireless Communication System Block Rates
    The student provided these inputs: {data}
    We calculated the following rates at the output of each block: {numerical_results}
    
    Please provide a clear, user-friendly explanation. For each block (Sampler, Quantizer, Source Coder, Channel Coder, Interleaver), explain:
    1.  What the block's purpose is in one simple sentence.
    2.  Why the data rate changed (or didn't change) at its output. For example, "The source coder compressed the data, reducing the rate..." or "The interleaver re-arranges bits to fight burst errors and does not change the data rate."
    Finally, explain how the burst duration was calculated from the final rate.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful engineering assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=400
        )
        ai_explanation = completion.choices[0].message.content.strip()
    except Exception as e:
        ai_explanation = f"Could not get AI explanation: {e}"

    return jsonify({
        "numericalResults": numerical_results,
        "aiExplanation": ai_explanation
    })
# Add this new endpoint to backend/app.py

@app.route("/api/ofdm-systems", methods=['POST'])
def handle_ofdm():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    numerical_results = calculate_ofdm_logic(data)
    if "error" in numerical_results:
        return jsonify(numerical_results), 400

    prompt = f"""
    Act as an expert wireless communications engineer explaining results to a student.

    Scenario: OFDM System Design
    The student provided these inputs: {data}
    Our calculations produced these results: {numerical_results}

    Please provide a clear, user-friendly explanation. Structure your response in three paragraphs:
    1.  **Methodology:** Briefly explain HOW the main results (like data rate and spectral efficiency) were calculated from the inputs.
    2.  **Results Explained:** Explain WHAT the results mean in practical terms. What does this data rate and efficiency signify for a real-world network?
    3.  **Conclusion:** A brief concluding sentence on the system's performance.
    Keep the tone educational and encouraging.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful engineering assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=350
        )
        ai_explanation = completion.choices[0].message.content.strip()
    except Exception as e:
        ai_explanation = f"Could not get AI explanation: {e}"

    return jsonify({
        "numericalResults": numerical_results,
        "aiExplanation": ai_explanation
    })
# Add this new endpoint to backend/app.py

@app.route("/api/link-budget", methods=['POST'])
def handle_link_budget():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    numerical_results = calculate_link_budget_logic(data)
    if "error" in numerical_results:
        return jsonify(numerical_results), 400

    prompt = f"""
    Act as an expert wireless communications engineer explaining results to a student.

    Scenario: Link Budget Calculation
    The student provided these inputs: {data}
    Our calculations produced these results: {numerical_results}
    
    Please provide a clear, user-friendly explanation. Structure your response in three paragraphs:
    1.  **Concept:** Briefly explain what a link budget is and why it's crucial for designing a reliable communication link.
    2.  **Methodology:** Explain how the Required Transmitted Power was calculated. Start from the receiver sensitivity and logically add all the losses and gains to arrive at the final number.
    3.  **Conclusion:** Explain the practical meaning of the Required Transmitted Power in Watts. What does this value tell the engineer about the type of transmitter they need to build or buy?
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful engineering assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=350
        )
        ai_explanation = completion.choices[0].message.content.strip()
    except Exception as e:
        ai_explanation = f"Could not get AI explanation: {e}"

    return jsonify({
        "numericalResults": numerical_results,
        "aiExplanation": ai_explanation
    })
# Add this final endpoint to backend/app.py

@app.route("/api/cellular-design", methods=['POST'])
def handle_cellular_design():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request body"}), 400

    numerical_results = calculate_cellular_design_logic(data)
    if "error" in numerical_results:
        return jsonify(numerical_results), 400

    prompt = f"""
    Act as an expert wireless communications engineer explaining results to a student.

    Scenario: Cellular System Design
    The student provided these inputs: {data}
    Our calculations produced these results: {numerical_results}
    
    Please provide a clear, user-friendly explanation. Structure your response in four paragraphs:
    1.  **Cell & Traffic Analysis:** Explain how the number of required cells was determined from the total area and cell radius. Then, explain how the total traffic was calculated in Erlangs and distributed per cell.
    2.  **Grade of Service (GoS):** Explain the concept of the Erlang B model and how it was used to find the 'Required Channels per Cell' to meet the desired blocking probability (Grade of Service).
    3.  **Frequency Reuse:** Explain what the 'Required Cluster Size (N)' means in the context of frequency reuse and managing co-channel interference (based on the provided SIR).
    4.  **Conclusion:** A brief concluding summary of the designed system's capacity.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful engineering assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=450
        )
        ai_explanation = completion.choices[0].message.content.strip()
    except Exception as e:
        ai_explanation = f"Could not get AI explanation: {e}"

    return jsonify({
        "numericalResults": numerical_results,
        "aiExplanation": ai_explanation
    })