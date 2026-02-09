FROM python:3.11-slim

# Create a non-root user (recommended)
RUN addgroup --system appgroup && adduser --system --ingroup appgroup appuser

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_NO_CACHE_DIR=1

# Install build deps if needed (kept small)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies first for layer caching
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# ensure gunicorn is available even if not listed in requirements
RUN pip install --no-cache-dir gunicorn

# Copy application code
COPY . .

# Give ownership to non-root user
RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 5000

# Launch with gunicorn. If your app import path differs, change "src.app.main:app"
CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:5000", "src.app.main:app"]

