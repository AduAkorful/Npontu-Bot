#!/bin/bash

PORT=${PORT:-5000}
exec gunicorn "back:create_app()" --bind "0.0.0.0:${PORT}" -w 4
