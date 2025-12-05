#!/bin/sh
set -e

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn nird_backend.wsgi:application --bind 0.0.0.0:$PORT
