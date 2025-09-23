#!/bin/bash
set -e

# Wait for PostgreSQL
echo "Waiting for postgres..."
sleep 5   # Small pause to let Docker DNS settle

while ! nc -z $DB_HOST $DB_PORT; do
  sleep 1
done
echo "PostgreSQL started"

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
exec "$@"