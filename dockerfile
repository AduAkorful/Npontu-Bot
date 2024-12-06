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

# Copy application code
COPY . /app

# Expose the application port
EXPOSE 5000

# Default command to run the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:${PORT:-5000}", "app:app"]

