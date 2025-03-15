from flask import Flask, request, jsonify, render_template
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from flask_cors import CORS

app = Flask(__name__, template_folder="templates")  # Définit le dossier pour index.html
CORS(app)

# Initialisation des moteurs d'analyse et d'anonymisation
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Stockage temporaire des anonymisations
anonymized_storage = {}

@app.route("/")
def home():
    return render_template("index.html")  # Affiche l'interface

@app.route("/anonymize", methods=["POST"])
def anonymize():
    """ Anonymisation du texte """
    data = request.get_json()
    if not data or "prompt" not in data:
        return jsonify({"error": "Missing 'prompt' field"}), 400

    text = data["prompt"]
    analysis = analyzer.analyze(text=text, language="en")
    anonymized = anonymizer.anonymize(text=text, analyzer_results=analysis)

    anonymized_storage[text] = anonymized.text  # Stocker pour recontextualisation
    return jsonify({"anonymized_text": anonymized.text})

@app.route("/recontextualize", methods=["POST"])
def recontextualize():
    """ Recontextualisation du texte après ChatGPT """
    data = request.get_json()
    if not data or "response" not in data:
        return jsonify({"error": "Missing 'response' field"}), 400

    response_text = data["response"]

    # Restaurer les données anonymisées
    for original, anonymized in anonymized_storage.items():
        if anonymized in response_text:
            response_text = response_text.replace(anonymized, original)

    return jsonify({"recontextualized_text": response_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
