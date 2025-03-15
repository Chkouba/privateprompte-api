FROM python:3.10-slim

# Installation des dépendances Python nécessaires
RUN pip install flask presidio-analyzer presidio-anonymizer requests flask-cors

# Installation du modèle SpaCy plus léger
RUN python -m spacy download en_core_web_sm

# Copie du fichier app.py
COPY app.py /app/app.py

# Définir le répertoire de travail
WORKDIR /app

# Copier l'application dans l'image Docker
COPY . /app
WORKDIR /app

# Commande pour lancer l’application
CMD ["python", "app.py"]
