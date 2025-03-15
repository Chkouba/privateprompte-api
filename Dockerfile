FROM python:3.10-slim

# Installation des dépendances Python nécessaires
RUN pip install flask presidio-analyzer presidio-anonymizer requests flask-cors

# Installation du modèle SpaCy français léger
RUN python -m spacy download fr_core_news_sm

# Copie du fichier app.py
COPY app.py /app/app.py

# Définir le répertoire de travail
WORKDIR /app

# Copier l'application dans l'image Docker
COPY . /app
WORKDIR /app

# Commande pour lancer l’application
CMD ["python", "app.py"]
