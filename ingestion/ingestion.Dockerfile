# ingestion.Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY . .
RUN pip install --no-cache-dir -r ingestion/requirements-ingestion.txt

CMD ["python", "-m", "ingestion.ingest"]