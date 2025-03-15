FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Installer le modèle SpaCy français léger
RUN python -m spacy download fr_core_news_sm

COPY . .

CMD ["python", "app.py"]
