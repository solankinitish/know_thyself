# ==========================================
# Stage 1: The Base Environment
# ==========================================
# We start with a slimmed-down Linux image that has Python 3.11 pre-installed
FROM python:3.11-slim AS base

# Prevent Python from writing .pyc files and keep stdout/stderr unbuffered for clean logging
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=off

WORKDIR /workspace

# Install system tools needed to compile certain Python ML packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy your dependencies list and install them inside the image
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your actual application code into the image
COPY app/ ./app/
COPY main.py .

COPY streamlit_app.py .

# ==========================================
# Stage 2: The Backend Runtime
# ==========================================
FROM base AS backend
EXPOSE 8000
# Tell the container to start your FastAPI app when it boots up
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

# ==========================================
# Stage 3: The Frontend Runtime
# ==========================================
FROM base AS frontend
EXPOSE 8501
# Point this directly to your root-level UI file!
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
