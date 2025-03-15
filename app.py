from flask import Flask, request, jsonify, render_template
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import SpacyNlpEngine
from presidio_anonymizer import AnonymizerEngine
import os
import spacy

app = Flask(__name__, template_folder="templates")

# Configure NLP engine
nlp_engine = SpacyNlpEngine()
nlp_engine.nlp = {"en": spacy.load("en_core_web_sm")}  # Utilisation en anglais

registry = RecognizerRegistry()
registry.load_predefined_recognizers(nlp_engine=nlp_engine, languages=["en"])
analyzer = AnalyzerEngine(registry=registry)
anonymizer = AnonymizerEngine()

# Stockage temporaire des anonymisations pour recontextualisation
anonymized_storage = {}

@app.route("/")
def home():
    return render_template("index.html")

@app.route('/anonymize', methods=['POST'])
def anonymize():
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "Field 'prompt' is required"}), 400

    prompt = data['prompt']
    analyzer_results = analyzer.analyze(text=prompt, language='en')

    anonymized_text = anonymizer.anonymize(text=prompt, analyzer_results=analyzer_results)

    # Stocker la correspondance entre original et anonymisé
    anonymized_storage[prompt] = anonymized_text.text

    return jsonify({"anonymized_text": anonymized_text.text})

@app.route('/recontextualize', methods=['POST'])
def recontextualize():
    data = request.get_json()
    if not data or 'response' not in data:
        return jsonify({"error": "Field 'response' is required"}), 400

    response_text = data['response']

    # Trouver le texte original correspondant à l'anonymisation
    for original, anonymized in anonymized_storage.items():
        if anonymized in response_text:
            response_text = response_text.replace(anonymized, original)

    return jsonify({"recontextualized_text": response_text})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))
