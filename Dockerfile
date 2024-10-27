# Dockerfile
FROM python:3.13-slim

# Install system utilities
RUN apt-get update && apt-get install -y procps psmisc

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY src/ ./src/

# Create directories for models and artifacts
RUN mkdir -p /app/models /app/artifacts

# Set environment variable
ENV PYTHONPATH=/app/src

# Entry point
ENTRYPOINT ["python", "-m", "src.hyperparameter_tuning"]
