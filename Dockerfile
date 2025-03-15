FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN python -m spacy download en_core_web_sm

COPY . .

CMD ["python", "app.py"]
