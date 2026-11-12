FROM python:3.12-slim AS builder

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

# Runner stage
FROM python:3.12-slim AS runner

WORKDIR /app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONPATH="/app/src" \
    PATH="/root/.local/bin:$PATH"

COPY --from=builder /root/.local /root/.local
COPY src/ /app/src/
COPY pyproject.toml /app/

EXPOSE 8000

CMD ["uvicorn", "urlsentinel.main:app", "--host", "0.0.0.0", "--port", "8000"]
