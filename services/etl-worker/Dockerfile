FROM python:3.11-slim

# Install system dependencies (required for some Python packages like psycopg2 or Pillow)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container
WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY src/ ./src/

# Set the Python path so local modules can be found
ENV PYTHONPATH=/app/src

# Default command to run the pipeline
CMD ["python", "src/main.py"]