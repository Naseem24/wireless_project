# backend/app.py (Final, Simple Version)
import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from groq import Groq
from calculations import calculate_wireless_system_logic, calculate_ofdm_logic, calculate_link_budget_logic, calculate_cellular_design_logic

load_dotenv()
app = Flask(__name__)

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    header['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
    header['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    return response

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ... The rest of the file (get_ai_explanation, create_api_endpoint, and all the routes) remains exactly the same as before ...
# (I am omitting it for brevity, but you can use the code from the previous working step)

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
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.4,
            max_tokens=400
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        return f"Could not get AI explanation: {e}"

def create_api_endpoint(calculation_function, scenario_name):
    data = request.get_json()
    numerical_results = calculation_function(data)
    ai_explanation = get_ai_explanation(scenario_name, data, numerical_results)
    return jsonify({
        "numericalResults": numerical_results,
        "aiExplanation": ai_explanation
    })

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