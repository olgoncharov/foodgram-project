#!/bin/bash

echo "Applying migrations"
django-admin migrate

echo "Collect static"
django-admin collectstatic --noinput

echo "Create or update django superuser"
python /helpers/create_or_update_superuser.py

echo "Running main programm"
gunicorn conf.wsgi:application --bind 0.0.0.0:8000