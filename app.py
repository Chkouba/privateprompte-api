from flask import Flask, request, jsonify, render_template, Response
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from flask_cors import CORS
import requests

app = Flask(__name__, template_folder="templates")
CORS(app)

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()
anonymized_storage = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/anonymize", methods=["POST"])
def anonymize():
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' field"}), 400

    text = data["prompt"]
    analysis = analyzer.analyze(text=text, language="en")
    anonymized = anonymizer.anonymize(text=text, analyzer_results=analysis)

    anonymized_storage[text] = anonymized.text
    return jsonify({"anonymized_text": anonymized.text})

@app.route("/recontextualize", methods=["POST"])
def recontextualize():
    data = request.get_json()
    if not data or "response" not in data:
        return jsonify({"error": "Missing 'response' field"}), 400

    response_text = data["response"]

    for original, anonymized in anonymized_storage.items():
        if anonymized in response_text:
            response_text = response_text.replace(anonymized, original)

    return jsonify({"recontextualized_text": response_text})

@app.route('/chatgpt-proxy')
def chatgpt_proxy():
    chatgpt_url = "https://chat.openai.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    response = requests.get(chatgpt_url, headers=headers)
    
    modified_headers = dict(response.headers)
    modified_headers.pop("Content-Security-Policy", None)
    modified_headers.pop("X-Frame-Options", None)
    
    return Response(
        response.content,
        status=response.status_code,
        headers=modified_headers,
        content_type=response.headers['Content-Type']
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
