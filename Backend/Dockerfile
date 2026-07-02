FROM python:3.11-slim AS base

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    poppler-utils \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Keep the Backend/ prefix intact so "Backend.app.xxx" imports keep working
COPY Backend ./Backend
COPY data ./data

RUN mkdir -p /app/medical_records

EXPOSE 8000

CMD ["sh", "-c", "uvicorn Backend.app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]