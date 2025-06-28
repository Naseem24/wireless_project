# backend/app.py (Final Production Version)
import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from openai import OpenAI
from calculations import calculate_wireless_system_logic, calculate_ofdm_logic, calculate_link_budget_logic, calculate_cellular_design_logic

load_dotenv()
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- Manual CORS Header Function ---
# This function is called after every request to add the necessary headers.
@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*' # Allow any domain to make requests
    header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    header['Access-Control-Allow-Methods'] = 'POST, OPTIONS' # Specify allowed methods
    return response


# --- Helper function for generating prompts ---
def get_ai_explanation(scenario_name, inputs, results):
    prompt = f"""
    Act as an expert wireless communications engineer explaining results to a student.

    Scenario: {scenario_name}
    The student provided these inputs: {inputs}
    Our calculations produced these results: {results}
    
    Please provide a clear, user-friendly explanation based on the scenario.
    For Wireless System, explain each block's impact on data rate.
    For OFDM, explain data rate and spectral efficiency.
    For Link Budget, explain the power calculation from sensitivity to gains/losses.
    For Cellular Design, explain cell count, traffic (Erlang B), and cluster size.
    Keep the tone educational and encouraging.
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=400
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Could not get AI explanation: {e}"

# --- Refactored API Endpoint ---
def create_api_endpoint(calculation_function, scenario_name):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Invalid request body"}), 400
    numerical_results = calculation_function(data)
    if "error" in numerical_results:
        return jsonify(numerical_results), 400
    ai_explanation = get_ai_explanation(scenario_name, data, numerical_results)
    return jsonify({
        "numericalResults": numerical_results,
        "aiExplanation": ai_explanation
    })

# --- Routes ---
@app.route("/api/wireless-system", methods=['POST'])
def handle_wireless_system():
    return create_api_endpoint(calculate_wireless_system_logic, "Wireless Communication System")

@app.route("/api/ofdm-systems", methods=['POST'])
def handle_ofdm():
    return create_api_endpoint(calculate_ofdm_logic, "OFDM System")

@app.route("/api/link-budget", methods=['POST'])
def handle_link_budget():
    return create_api_endpoint(calculate_link_budget_logic, "Link Budget Calculation")

@app.route("/api/cellular-design", methods=['POST'])
def handle_cellular_design():
    return create_api_endpoint(calculate_cellular_design_logic, "Cellular System Design")