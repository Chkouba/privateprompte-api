from flask import Flask, request, jsonify
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import SpacyNlpEngine
from presidio_anonymizer import AnonymizerEngine
import os
import spacy

app = Flask(__name__)

# Ensure the English model is downloaded
spacy.cli.download("en_core_web_sm")

# Configure the NLP engine to use the English model
nlp_engine = SpacyNlpEngine()
nlp_engine.nlp = {}
nlp_engine.nlp["en"] = spacy.load("en_core_web_sm")

registry = RecognizerRegistry()
registry.load_predefined_recognizers(nlp_engine=nlp_engine, languages=["en"])
analyzer = AnalyzerEngine(registry=registry)
anonymizer = AnonymizerEngine()

@app.route('/anonymize', methods=['GET', 'POST'])
def anonymize():
    if request.method == 'GET':
        return jsonify({"message": "Use a POST request with a JSON containing 'prompt'."})

    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "The 'prompt' field is required"}), 400

    prompt = data['prompt']
    analyzer_results = analyzer.analyze(text=prompt, language='en')
    anonymized_text = anonymizer.anonymize(text=prompt, analyzer_results=analyzer_results)

    return jsonify({"anonymized_text": anonymized_text.text})

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "API is running"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))
