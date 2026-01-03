from flask import Flask, jsonify
from flask_cors import CORS
import random
import os
import requests

# --------------------------------
# Read API key from OS environment
# --------------------------------
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# --------------------------------
# Flask App Setup
# --------------------------------
app = Flask(__name__)
CORS(app)

# --------------------------------
# Baseline values
# --------------------------------
BASELINE_LATENCY = (180, 250)   # ms
BASELINE_OUTPUT = (1.1, 1.3)    # KB

# --------------------------------
# Simulate system metrics (TRUE + FALSE)
# --------------------------------
def simulate_metrics():
    silent_failure = random.choice([True, False])

    if silent_failure:
        latency = random.randint(500, 800)
        output_size = round(random.uniform(0.6, 0.8), 2)
    else:
        latency = random.randint(*BASELINE_LATENCY)
        output_size = round(random.uniform(*BASELINE_OUTPUT), 2)

    return latency, output_size, silent_failure

# --------------------------------
# Gemini 2.0 Flash (REST API)
# --------------------------------
def gemini_explanation(latency, output_size):
    try:
        url = (
            "https://generativelanguage.googleapis.com/v1beta/models/"
            "gemini-2.0-flash:generateContent"
            f"?key={GEMINI_API_KEY}"
        )

        prompt = f"""
You are a system reliability assistant.

Normal behavior:
Latency: {BASELINE_LATENCY[0]}–{BASELINE_LATENCY[1]} ms
Output size: {BASELINE_OUTPUT[0]}–{BASELINE_OUTPUT[1]} KB

Current behavior:
Latency: {latency} ms
Output size: {output_size} KB

Explain briefly why this represents a silent failure.
"""

        payload = {
            "contents": [
                {
                    "parts": [{"text": prompt}]
                }
            ]
        }

        response = requests.post(url, json=payload)

        if response.status_code == 429:
            return "Gemini API rate-limited. AI explanation temporarily unavailable."

        if response.status_code == 404:
            return "Gemini model endpoint not accessible for this account or network."

        if response.status_code != 200:
            return f"Gemini error (status {response.status_code})."

        return response.json()["candidates"][0]["content"]["parts"][0]["text"]

    except Exception:
        return "Gemini service unavailable."

# --------------------------------
# API Endpoint
# --------------------------------
@app.route("/status")
def status():
    latency, output_size, silent_failure = simulate_metrics()

    if silent_failure:
        explanation = gemini_explanation(latency, output_size)
    else:
        explanation = "System behavior is within the normal baseline range."

    return jsonify({
        "system_status": "Running",
        "silent_failure": silent_failure,
        "latency_ms": latency,
        "output_size_kb": output_size,
        "explanation": explanation
    })

# --------------------------------
# Run Server (NO debug mode)
# --------------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
