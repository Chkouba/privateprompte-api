FROM python:3.10-slim

# Installation des dépendances Python nécessaires
RUN pip install flask presidio-analyzer presidio-anonymizer requests flask-cors

# Copie du fichier app.py
COPY app.py /app/app.py

# Définir le répertoire de travail
WORKDIR /app

# Copier l'application dans l'image Docker
COPY . /app
WORKDIR /app

# Installer Flask, requests et presidio-analyzer/anonymizer
RUN pip install flask requests presidio-analyzer presidio-anonymizer

# Commande pour lancer l’application
CMD ["python", "app.py"]
