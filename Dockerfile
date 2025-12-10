FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements_api.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements_api.txt

# Copy application files
COPY api.py .

# Create saved_models directory for local testing
RUN mkdir -p saved_models

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "api.py"]
