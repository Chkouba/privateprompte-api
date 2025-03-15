FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc python3-dev

COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

COPY templates/ /app/templates/
COPY static/ /app/static/
COPY app.py .

CMD ["python", "app.py"]
