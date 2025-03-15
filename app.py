from flask import Flask, request, jsonify
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

app = Flask(__name__)

# Initialiser les moteurs de Presidio
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

@app.route('/anonymize', methods=['POST'])
def anonymize_prompt():
    data = request.get_json()
    prompt = data.get('prompt', '')

    # Analyser le texte (identification des infos sensibles)
    analyzer_results = analyzer.analyze(text=prompt, language='fr')

    # Anonymiser le texte
    anonymized_text = anonymizer.anonymize(text=prompt, analyzer_results=analyzer_results)

    return jsonify({"anonymized_text": anonymized_text.text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
