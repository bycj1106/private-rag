FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

ENV PYTHONPATH=/app
ENV CHROMA_DIR=/app/data/chroma
ENV DB_PATH=/app/data/app.db

RUN mkdir -p /app/data

EXPOSE 8000

CMD ["python3", "-m", "app.main"]
