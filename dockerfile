# Use a lightweight Python base image
FROM python:3.9-slim-bullseye

# Set the working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libffi-dev \
    python3-dev \
    build-essential \
    libjpeg-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set Python environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy the requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools \
    && pip install --no-cache-dir -r /app/requirements.txt

# Decode and create the client_secret.json file from the environment variable
ENV CLIENT_SECRET_JSON_B64="eyJ3ZWIiOnsiY2xpZW50X2lkIjoiODY5MTU5NTA2Mjc4LWZvb3RnbTF2ZTllMnJnNTJsaWdsazUybGExcjJjazJpLmFwcHMuZ29vZ2xldXNlcmNvbnRlbnQuY29tIiwicHJvamVjdF9pZCI6Imdlbi1sYW5nLWNsaWVudC0wMzMxMDcxODMzIiwiYXV0aF91cmkiOiJodHRwczovL2FjY291bnRzLmdvb2dsZS5jb20vby9vYXV0aDIvYXV0aCIsInRva2VuX3VyaSI6Imh0dHBzOi8vb2F1dGgyLmdvb2dsZWFwaXMuY29tL3Rva2VuIiwiYXV0aF9wcm92aWRlcl94NTA5X2NlcnRfdXJsIjoiaHR0cHM6Ly93d3cuZ29vZ2xlYXBpcy5jb20vb2F1dGgyL3YxL2NlcnRzIiwiY2xpZW50X3NlY3JldCI6IkdPQ1NQWC1pbEktSmRPdGVUeTZlVnNkVlBNUHlLMTYwanlUIiwicmVkaXJlY3RfdXJpcyI6WyJodHRwczovL2phY2thbC1zdWl0YWJsZS1tYW5hdGVlLm5ncm9rLWZyZWUuYXBwIl19fQ=="

# Copy application code
COPY . /app

# Make the start script executable (if used)
RUN chmod +x /app/start.sh

# Expose the application port
EXPOSE 5000

# Use a shell script to handle PORT or default
CMD ["/app/start.sh"]

