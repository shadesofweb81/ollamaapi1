FROM python:3.12-slim

WORKDIR /app

# Install build tools required for uvicorn[standard] (uvloop, httptools)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY src/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY src/ .

EXPOSE 8000

# NOTE: The app connects to Ollama at http://localhost:11434 (hardcoded in main.py).
# When running in Docker, set OLLAMA_HOST env var or update the host to point to
# your Ollama instance (e.g., host.docker.internal:11434 on Docker Desktop).
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
