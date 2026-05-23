# syntax=docker/dockerfile:1

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . .

# Collect static files and apply migrations
RUN python manage.py collectstatic --noinput
RUN python manage.py migrate --noinput

EXPOSE 8000

# Run the application with gunicorn
CMD ["gunicorn", "pet_care_management.wsgi:application", "--bind", "0.0.0.0:8000"]
