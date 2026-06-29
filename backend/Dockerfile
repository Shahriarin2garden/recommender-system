# Build context must be repo root: docker build -f backend/Dockerfile .
FROM python:3.11-slim as builder

WORKDIR /app

RUN apt-get update && apt-get install -y gcc postgresql-client && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Production stage
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

COPY --from=builder /root/.local /home/appuser/.local

# Copy backend app
COPY backend/app ./app
COPY backend/seed_data.py .
COPY backend/train_model.py .

# Copy ML model artifacts
COPY ml/ ./ml/

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
ENV PATH=/home/appuser/.local/bin:$PATH
USER appuser

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

CMD uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}
