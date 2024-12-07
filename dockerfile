# Multi-stage Dockerfile to handle both PHP frontend and Python backend

# Stage 1: Set up PHP for the frontend
FROM php:8.1-apache AS frontend

# Copy the PHP frontend file (index.php) to Apache's document root
COPY index.php /var/www/html/

# Optional: Copy assets like images, CSS, or JS if needed
COPY static/ /var/www/html/static/

# Enable Apache rewrite module if required
RUN a2enmod rewrite

# Stage 2: Set up Python for the backend
FROM python:3.9-slim-bullseye AS backend

# Set the working directory for the Python backend
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

# Copy the Python requirements file and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip setuptools \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy the Python backend files
COPY back.py /app/
COPY start.sh /app/

# Make the start script executable
RUN chmod +x /app/start.sh

# Expose ports for PHP (frontend) and Python (backend)
EXPOSE 80
EXPOSE 5000

# Combine both PHP and Python setups
CMD ["/app/start.sh"]
