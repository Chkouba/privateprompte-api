# Utilisation d'une image Python légère
FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier et installer les dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Télécharger les modèles SpaCy séparément (évite les erreurs)
RUN python -m spacy download fr_core_news_sm
RUN python -m spacy download en_core_web_sm || true  # Ignore l'erreur si non dispo

# Copier tous les fichiers du projet
COPY . .

# Exposer le port 8000
EXPOSE 8000

# Démarrer l'application Flask avec gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
