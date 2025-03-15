FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Télécharger les modèles SpaCy
RUN python -m spacy download fr_core_news_sm && \
    python -m spacy download en_core_web_sm

COPY . .

CMD ["python", "app.py"]
