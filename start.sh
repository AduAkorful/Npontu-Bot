#!/bin/bash

# Debugging PATH
echo "Current PATH: $PATH"

# Ensure Gunicorn is accessible
export PATH=$PATH:/usr/local/bin:/usr/local/sbin:/usr/bin:/bin:/usr/sbin:/sbin

# Set the PORT environment variable or default to 5000
PORT=${PORT:-5000}

# Debugging gunicorn availability
if ! which gunicorn > /dev/null 2>&1; then
    echo "Gunicorn not found in PATH"
    exit 1
fi

# Debugging Python environment
echo "Python version: $(python3 --version)"
echo "Gunicorn version: $(gunicorn --version)"

# Launch Gunicorn with the application factory
exec gunicorn "back:create_app()" --bind "0.0.0.0:${PORT}" -w 4
