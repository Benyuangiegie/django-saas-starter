# Use official Python 3.13 slim image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    DJANGO_SETTINGS_MODULE=core.settings

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev netcat-traditional \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Copy entrypoint
COPY entrypoint.prod.sh /app/entrypoint.prod.sh
USER root
RUN chmod +x /app/entrypoint.prod.sh
USER appuser

# Expose port
EXPOSE 8000

# Set entrypoint script
ENTRYPOINT ["/app/entrypoint.prod.sh"]

# Run Gunicorn server
CMD ["gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000", "--workers=4", "--threads=2", "--timeout=120", "--access-logfile", "-", "--error-logfile", "-"]