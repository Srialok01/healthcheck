# Use Python 3.9 slim image as base
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app && chown -R app:app /app
USER app

# Expose port (optional, for future web interface)
EXPOSE 8000

# Default command to run the example usage
CMD ["python", "example_usage.py"]

# Alternative commands you can use:
# CMD ["python", "api.py", "https://google.com", "--summary"]
# CMD ["python", "api.py", "https://google.com", "https://github.com", "--json"]