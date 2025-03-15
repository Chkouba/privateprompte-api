from flask import Flask, request, jsonify
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
import os

app = Flask(__name__)

analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

@app.route('/anonymize', methods=['POST'])
def anonymize():
    data = request.get_json()
    prompt = data.get('prompt', '')

    analyzer_results = analyzer.analyze(text=prompt, language='fr')
    anonymized_text = anonymizer.anonymize(text=prompt, analyzer_results=analyzer_results)

    return jsonify({"anonymized_text": anonymized_text.text})

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "API is running"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))
