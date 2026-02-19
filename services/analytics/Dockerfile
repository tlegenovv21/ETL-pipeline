# services/analytics/Dockerfile

FROM python:3.11-slim

WORKDIR /app

# Copy the requirements file you created earlier
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Streamlit application code
COPY app.py .

# Expose the default Streamlit port
EXPOSE 8501

# Command to run the Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]