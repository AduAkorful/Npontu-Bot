# Stage 1: Python dependencies
FROM python:3.9-slim-bullseye as python-build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Stage 2: PHP + Python
FROM php:8.1-apache
WORKDIR /app

# Install Python runtime
RUN apt-get update && apt-get install -y python3 && apt-get clean

# Copy Python dependencies
COPY --from=python-build /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages

# Copy application code
COPY . .

# Serve PHP and Python
RUN a2enmod rewrite
RUN echo "ProxyPass /api http://127.0.0.1:5000/" >> /etc/apache2/sites-enabled/000-default.conf

CMD ["/app/start.sh"]
