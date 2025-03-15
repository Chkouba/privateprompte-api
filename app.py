from flask import Flask, request, jsonify, Response
import requests
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Autorise les requêtes cross-origin

# Initialisation de l'anonymiseur
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# URL de ChatGPT (il peut changer si OpenAI modifie son API publique)
CHATGPT_URL = "https://chat.openai.com/backend-api/conversation"

def anonymize_text(text):
    """ Anonymise le texte avant de l'envoyer à ChatGPT """
    results = analyzer.analyze(text=text, language='en')
    anonymized = anonymizer.anonymize(text=text, analyzer_results=results)
    return anonymized.text

def recontextualize_text(original, response):
    """ Recontextualise la réponse en remplaçant les données anonymisées """
    for entity in original:
        if original[entity] in response:
            response = response.replace(original[entity], entity)
    return response

@app.route("/", methods=["GET"])
def home():
    return "Proxy inversé Private Prompt en cours d'exécution !"

@app.route("/proxy", methods=["POST"])
def proxy_chatgpt():
    """ Redirige et modifie les requêtes vers ChatGPT """
    user_input = request.json.get("prompt", "")
    if not user_input:
        return jsonify({"error": "Prompt manquant"}), 400

    # Anonymisation avant l'envoi
    anonymized_text = anonymize_text(user_input)

    # Envoyer la requête anonymisée à ChatGPT
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {request.headers.get('Authorization', '')}"
    }
    data = {"model": "text-davinci-003", "prompt": anonymized_text, "max_tokens": 200}

    chat_response = requests.post(CHATGPT_URL, json=data, headers=headers)

    if chat_response.status_code != 200:
        return jsonify({"error": "Erreur de communication avec ChatGPT"}), chat_response.status_code

    chat_response_json = chat_response.json()
    chatgpt_reply = chat_response_json.get("choices", [{}])[0].get("text", "")

    # Recontextualisation automatique
    recontextualized_text = recontextualize_text({user_input: anonymized_text}, chatgpt_reply)

    return jsonify({"response": recontextualized_text})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
