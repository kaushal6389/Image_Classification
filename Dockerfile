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

# Create saved_models directory (model will be downloaded from Google Drive on startup)
RUN mkdir -p saved_models

# Expose port (Railway will set PORT env variable)
EXPOSE 8000

# Run the application (api.py handles PORT env variable)
CMD ["python", "api.py"]
