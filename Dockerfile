FROM python:3.11-slim

# Set environment variables for better logging
ENV PYTHONUNBUFFERED=1

# Create app directory
WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    default-libmysqlclient-dev \
    pkg-config \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Bundle app source
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash app
RUN chown -R app:app /usr/src/app
USER app

# Purely informational! Has no effect on the build command
EXPOSE 3011

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:3011", "--workers", "3", "geobin.wsgi:application"]