from flask import Flask, request, jsonify, render_template, Response
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from flask_cors import CORS
import requests

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()
session_storage = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/anonymize", methods=["POST"])
def anonymize():
    data = request.get_json()
    text = data.get("prompt", "")
    session_id = data.get("session", "")
    
    analysis = analyzer.analyze(text=text, language="en")
    anonymized = anonymizer.anonymize(text=text, analyzer_results=analysis)
    
    session_storage[session_id] = {
        "mapping": {text: anonymized.text}
    }
    
    return jsonify({"anonymized_text": anonymized.text})

@app.route("/recontextualize", methods=["POST"])
def recontextualize():
    data = request.get_json()
    response_text = data.get("response", "")
    session_id = data.get("session", "")
    
    mappings = session_storage.get(session_id, {}).get("mapping", {})
    
    for original, anonymized in mappings.items():
        response_text = response_text.replace(anonymized, original)
    
    return jsonify({"recontextualized_text": response_text})

@app.route('/chatgpt-proxy/<path:subpath>', methods=['GET', 'POST'])
def chatgpt_proxy(subpath=""):
    base_url = "https://chat.openai.com"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    
    try:
        response = requests.request(
            method=request.method,
            url=f"{base_url}/{subpath}",
            headers=headers,
            data=request.get_data(),
            timeout=10
        )
        
        return Response(
            response.content,
            status=response.status_code,
            headers={"Content-Type": response.headers["Content-Type"]}
        )
        
    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
