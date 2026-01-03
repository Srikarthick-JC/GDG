from flask import Flask, jsonify
from flask_cors import CORS
import random
import os

# Try importing Gemini (safe)
try:
    from google import genai
    GEMINI_AVAILABLE = True
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
except Exception:
    GEMINI_AVAILABLE = False

# -------------------------------
# Flask App Setup
# -------------------------------
app = Flask(__name__)
CORS(app)

# -------------------------------
# Baseline (Normal Behavior)
# -------------------------------
BASELINE_LATENCY = (180, 250)   # ms
BASELINE_OUTPUT = (1.1, 1.3)    # KB

# -------------------------------
# Simulate Metrics
# -------------------------------
def simulate_metrics():
    silent_failure = random.choice([True, False])  # BOTH cases

    if silent_failure:
        latency = random.randint(500, 800)
        output_size = round(random.uniform(0.6, 0.8), 2)
    else:
        latency = random.randint(*BASELINE_LATENCY)
        output_size = round(random.uniform(*BASELINE_OUTPUT), 2)

    return latency, output_size, silent_failure

# -------------------------------
# Gemini / AI Explanation
# -------------------------------
def ai_explanation(latency, output_size):
    # --- Try Gemini first ---
    if GEMINI_AVAILABLE:
        try:
            prompt = f"""
You are a system reliability assistant.

Normal system behavior:
Latency: {BASELINE_LATENCY[0]}–{BASELINE_LATENCY[1]} ms
Output size: {BASELINE_OUTPUT[0]}–{BASELINE_OUTPUT[1]} KB

Current system behavior:
Latency: {latency} ms
Output size: {output_size} KB

Explain briefly why this is a silent failure.
"""

            response = client.models.generate_content(
                model="models/gemini-1.0-pro",
                contents=prompt
            )
            return response.text
        except Exception:
            pass  # Fall back safely

    # --- Fallback explanation (always works) ---
    return (
        f"Silent failure detected: latency ({latency} ms) and output size "
        f"({output_size} KB) deviate from the baseline without explicit errors, "
        f"indicating degraded internal processing or partial service malfunction."
    )

# -------------------------------
# API Endpoint
# -------------------------------
@app.route("/status")
def status():
    latency, output_size, silent_failure = simulate_metrics()

    if silent_failure:
        explanation = ai_explanation(latency, output_size)
    else:
        explanation = "System behavior is within the normal baseline range."

    return jsonify({
        "system_status": "Running",
        "silent_failure": silent_failure,
        "latency_ms": latency,
        "output_size_kb": output_size,
        "explanation": explanation
    })

# -------------------------------
# Run Server
# -------------------------------
if __name__ == "__main__":
    app.run(debug=True)
