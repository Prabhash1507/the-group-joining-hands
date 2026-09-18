# Use lightweight Python 3.10 slim base image
# Force rebuild trigger for Render deployment sync
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Copy application files into container
COPY . /app

# Install dependencies if present
RUN pip install --no-cache-dir -r requirements.txt

# Expose default server port
EXPOSE 10000

# Environment variables
ENV HOST=0.0.0.0
ENV PORT=10000
ENV APP_ENV=production
ENV PYTHONUNBUFFERED=1

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import os, urllib.request; urllib.request.urlopen('http://127.0.0.1:' + os.environ.get('PORT', '10000') + '/health')" || exit 1

# Command to run server on startup
CMD ["python", "server.py"]
