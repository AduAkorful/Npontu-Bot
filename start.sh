#!/bin/bash

# Set default port if not provided
PORT=${PORT:-5000}

# Debugging: Print the port being used
echo "Starting application on port: $PORT"

# Start the Gunicorn server
exec gunicorn back:app --bind 0.0.0.0:$PORT -w 4
