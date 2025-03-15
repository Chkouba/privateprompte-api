from flask import Flask, request, jsonify
from presidio_analyzer import AnalyzerEngine, RecognizerRegistry
from presidio_analyzer.nlp_engine import SpacyNlpEngine
from presidio_anonymizer import AnonymizerEngine
import os
import spacy

app = Flask(__name__)

# Configure le moteur NLP pour utiliser le modèle français léger
nlp_engine = SpacyNlpEngine()  # Sans utiliser 'model_name'
nlp_engine.nlp = {}  # Initialiser le dictionnaire
nlp_engine.nlp["fr"] = spacy.load("fr_core_news_sm")

registry = RecognizerRegistry()
registry.load_predefined_recognizers(nlp_engine=nlp_engine, languages=["fr"])
analyzer = AnalyzerEngine(registry=registry)
anonymizer = AnonymizerEngine()

@app.route('/anonymize', methods=['GET', 'POST'])
def anonymize():
    if request.method == 'GET':
        return jsonify({"message": "Utilisez une requête POST avec un JSON contenant 'prompt'."})
    
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "Le champ 'prompt' est requis"}), 400

    prompt = data['prompt']
    analyzer_results = analyzer.analyze(text=prompt, language='fr')
    anonymized_text = anonymizer.anonymize(text=prompt, analyzer_results=analyzer_results)
    
    return jsonify({"anonymized_text": anonymized_text.text})

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "API is running"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 8000)))
