# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy Python requirements first (for better caching)
COPY python/requirements.txt /app/python/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/python/requirements.txt

# Install Flask and CORS
RUN pip install --no-cache-dir flask flask-cors

# Install openpyxl for Excel export
RUN pip install --no-cache-dir openpyxl

# Copy application code
COPY . /app

# Expose port
EXPOSE 5000

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV FLASK_APP=app_server.py

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/api/health')"

# Run the Flask app
CMD ["python", "app_server.py"]
