# Use a base image that supports both PHP and Python
FROM php:8.1-apache

# Set the working directory for the application
WORKDIR /app

# Install Python and required system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    libpq-dev \
    libffi-dev \
    python3-dev \
    gcc \
    build-essential \
    libjpeg-dev \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the PHP frontend code to the Apache root directory
COPY index.php /var/www/html/
COPY bg.png /var/www/html/
COPY picture.png /var/www/html/

# Install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip3 install --no-cache-dir --upgrade pip setuptools \
    && pip3 install --no-cache-dir -r /app/requirements.txt

# Copy the Python backend code
COPY . /app

# Set up Apache to serve PHP and configure backend proxy
RUN a2enmod rewrite proxy_http
RUN echo "\
    <VirtualHost *:80>\n\
        DocumentRoot /var/www/html\n\
        <Directory /var/www/html>\n\
            Options Indexes FollowSymLinks\n\
            AllowOverride All\n\
            Require all granted\n\
        </Directory>\n\
        ProxyPass /api http://127.0.0.1:5000/\n\
        ProxyPassReverse /api http://127.0.0.1:5000/\n\
    </VirtualHost>" > /etc/apache2/sites-enabled/000-default.conf

# Make the start script executable
RUN chmod +x /app/start.sh

# Expose ports for both services
EXPOSE 80
EXPOSE 5000

# Start both Apache and Gunicorn
CMD ["/app/start.sh"]
