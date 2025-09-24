#!/bin/bash
set -e

echo "Installing Python dependencies..."
pip install -r requirements-dev.txt

echo "Running migrations..."
python manage.py migrate

echo "Development environment setup complete!"