#!/bin/bash
set -e

# 1. Apply Migrations (This fixes the 500 Server Error)
echo "Applying database migrations..."
python manage.py migrate --noinput

# 2. Start the Gunicorn web server
echo "Starting Gunicorn server..."
# Gunicorn can now find the wsgi module because the file structure is correct.
gunicorn string_analyzer_project.wsgi