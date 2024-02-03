#!/bin/sh

# Run migrations and then start the server
python manage.py makemigrations service ticket
python manage.py migrate
#gunicorn --config gunicorn.conf.py your_django_project.wsgi:application