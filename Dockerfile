# Multi-stage build for Strafrecht Online Django Application
FROM node:18-alpine AS frontend-builder

# Set working directory for frontend build
WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm ci --only=production --legacy-peer-deps

# Copy frontend source code
COPY frontend/ ./

# Build frontend assets
RUN npm run build

# Main application stage
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app \
    DJANGO_SETTINGS_MODULE=app.settings \
    PORT=8000

# Create app user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    libgdal-dev \
    gdal-bin \
    gettext \
    curl \
    libffi-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Copy requirements files
COPY requirements/ ./requirements/

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements/production.txt

# Copy forked dependencies and install them
COPY wagtail-birdsong-fork/ ./wagtail-birdsong-fork/
COPY strafrecht-wagtailcomments-xtd-fork/ ./strafrecht-wagtailcomments-xtd-fork/

RUN pip install -e ./wagtail-birdsong-fork && \
    pip install -e ./strafrecht-wagtailcomments-xtd-fork

# Copy application code
COPY . .

# Copy built frontend assets from frontend-builder stage
COPY --from=frontend-builder /app/frontend/build ./frontend/build

# Create necessary directories
RUN mkdir -p /app/staticfiles /app/media /app/log && \
    chown -R appuser:appuser /app

# Collect static files
RUN python manage.py collectstatic --noinput

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/admin/login/ || exit 1

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "120", "app.wsgi:application"]
