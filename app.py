from flask import Flask, request, jsonify
import requests
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)  # Autoriser les requêtes cross-origin

# Initialisation des moteurs d'analyse et d'anonymisation
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Stockage temporaire des anonymisations
anonymized_storage = {}

# URL de ChatGPT (modification selon API)
CHATGPT_URL = "https://chat.openai.com/backend-api/conversation"

def anonymize_text(text):
    """ Anonymise le texte de l'utilisateur """
    results = analyzer.analyze(text=text, language='en')
    anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
    anonymized_storage[text] = anonymized.text  # Stocker pour recontextualisation
    return anonymized.text

def recontextualize_text(response_text):
    """ Recontextualise la réponse de ChatGPT """
    for original, anonymized in anonymized_storage.items():
        if anonymized in response_text:
            response_text = response_text.replace(anonymized, original)
    return response_text

@app.route("/", methods=["GET"])
def home():
    return "Private Prompt API is running!"

@app.route("/anonymize", methods=["POST"])
def anonymize():
    """ Anonymisation avant d'envoyer à ChatGPT """
    data = request.get_json()
    if not data or 'prompt' not in data:
        return jsonify({"error": "Missing prompt"}), 400

    anonymized_text = anonymize_text(data['prompt'])
    return jsonify({"anonymized_text": anonymized_text})

@app.route("/recontextualize", methods=["POST"])
def recontextualize():
    """ Recontextualisation après la réponse de ChatGPT """
    data = request.get_json()
    if not data or 'response' not in data:
        return jsonify({"error": "Missing response"}), 400

    recontextualized_text = recontextualize_text(data['response'])
    return jsonify({"recontextualized_text": recontextualized_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
