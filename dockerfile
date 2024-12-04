# Stage 1: Install dependencies
FROM python:3.9-bullseye AS builder

# Set working directory
WORKDIR /app

# Copy requirements file first for caching
COPY requirements.txt /app/requirements.txt

# Install system dependencies and Python libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    libffi-dev \
    python3-dev \
    build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir --upgrade pip setuptools \
    && pip install --no-cache-dir -r requirements.txt

# Stage 2: Build the final image
FROM python:3.9-bullseye

# Set working directory
WORKDIR /app

# Copy installed dependencies and application code
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
COPY . /app

# Expose the application port
EXPOSE 5000

# Start the application
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
