# Dockerfile
FROM python:3.8-slim-buster

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /KhedmatkarBackend

# Install dependencies
RUN pip install --no-cache-dir django==3.2.8 psycopg2-binary==2.9.1 gunicorn==20.1.0

# Copy project
COPY . /KhedmatkarBackend/

# Run gunicorn
CMD ["gunicorn", "--config", "gunicorn.conf.py", "your_django_project.wsgi:application"]