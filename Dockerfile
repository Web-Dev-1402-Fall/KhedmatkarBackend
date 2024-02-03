# Dockerfile
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /KhedmatkarBackend

# Update package lists, install nc, django-cors-headers, djangorestframework and drf-yasg
RUN apt-get update && apt-get install -y netcat && pip install django-cors-headers djangorestframework drf-yasg requests

# Install Python dependencies
RUN pip install --no-cache-dir django==3.2.8 psycopg2-binary==2.9.1 gunicorn==20.1.0

# Copy project
COPY . /KhedmatkarBackend/

# Copy entrypoint.sh
COPY ./entrypoint.sh /KhedmatkarBackend/entrypoint.sh

# Make entrypoint.sh executable
RUN chmod +x /KhedmatkarBackend/entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT ["/KhedmatkarBackend/entrypoint.sh"]