# ============================================
# Multi-stage Build - Stage 1: Builder
# ============================================
FROM python:3.12-alpine AS builder

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies required for building Python packages
RUN apk add --no-cache \
    postgresql-dev \
    gcc \
    musl-dev \
    linux-headers

# Create and set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install --user --no-warn-script-location -r requirements.txt

# ============================================
# Stage 2: Runtime
# ============================================
FROM python:3.12-alpine

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/appuser/.local/bin:$PATH

# Install runtime dependencies only
RUN apk add --no-cache \
    postgresql-libs \
    bash \
    netcat-openbsd

# Create non-root user for security
RUN addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder /root/.local /home/appuser/.local

# Copy project files
COPY --chown=appuser:appuser . .

# Copy and set permissions for entrypoint script
COPY --chown=appuser:appuser entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Create directories for static and media files
RUN mkdir -p /app/staticfiles /app/media && \
    chown -R appuser:appuser /app/staticfiles /app/media

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:8000/admin/', timeout=5)" || exit 1

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]

# Default command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--timeout", "60", "--access-logfile", "-", "--error-logfile", "-", "backend.wsgi:application"]
