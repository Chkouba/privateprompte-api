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
    text = data.get("prompt", "")
    
    analysis = analyzer.analyze(text=text, language="en")
    anonymized = anonymizer.anonymize(text=text, analyzer_results=analysis)
    
    anonymized_storage[text] = anonymized.text
    return jsonify({"anonymized_text": anonymized.text})

@app.route("/recontextualize", methods=["POST"])
def recontextualize():
    data = request.get_json()
    response_text = data.get("response", "")
    
    for original, anonymized in anonymized_storage.items():
        response_text = response_text.replace(anonymized, original)
    
    return jsonify({"recontextualized_text": response_text})

@app.route('/chatgpt-proxy')
def chatgpt_proxy():
    response = requests.get("https://chat.openai.com", headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    })
    
    return Response(
        response.content,
        headers={
            "Content-Type": response.headers["Content-Type"],
            "Cache-Control": "no-cache"
        },
        status=response.status_code
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
