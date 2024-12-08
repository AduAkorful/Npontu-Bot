#!/bin/bash

# Set the PORT environment variable or default to 5000
PORT=${PORT:-5000}

# Launch Gunicorn with the application factory
gunicorn "back:create_app()" --bind "0.0.0.0:${PORT}" --workers 4 --timeout 120
