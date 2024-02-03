#!/bin/bash

# Install requirements
pip install -r requirements.txt

#
python3 manage.py makemigrations

# Migrate database
python3 manage.py migrate

# Start server
python3 manage.py runserver 0.0.0.0:8000
