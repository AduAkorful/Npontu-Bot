#!/bin/bash

# Debugging PATH
echo "Current PATH: $PATH"

# Ensure Gunicorn is accessible
export PATH=$PATH:~/.local/bin

# Set the PORT environment variable or default to 5000
PORT=${PORT:-5000}

# Debugging gunicorn availability
which gunicorn || { echo "Gunicorn not found in PATH"; exit 1; }

# Launch Gunicorn with the application factory
exec /usr/local/bin/gunicorn "back:create_app()" --bind "0.0.0.0:${PORT}" -w 4
