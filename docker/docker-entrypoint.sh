#!/bin/bash

echo "Collect static"
django-admin collectstatic --noinput

echo "Create or update django superuser"
python entrypoint.py

echo "Running main programm"
gunicorn conf.wsgi:application --bind 0.0.0.0:8000