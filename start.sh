#!/bin/bash

# Set the PORT environment variable or default to 5000
PORT=${PORT:-5000}

# Start Apache in the background for the PHP frontend
service apache2 start

# Launch Gunicorn with the application factory
exec gunicorn "back:create_app()" --bind "0.0.0.0:${PORT}" -w 4
