# Use the official lightweight Python image
FROM python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Ensure the client_secret.json file has appropriate permissions
RUN chmod 644 /app/client_secret.json

# Expose the port the application runs on
EXPOSE 5000

# Set environment variables, if needed
# ENV FLASK_APP=back.py

# Use Gunicorn to serve the application
CMD ["gunicorn", "-b", "0.0.0.0:5000", "back:create_app()"]
