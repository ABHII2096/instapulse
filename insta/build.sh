#!/usr/bin/env bash
set -o errexit

# This line MUST be first to install Django
pip install -r requirements.txt

# These lines run after Django is installed
python manage.py collectstatic --no-input
python manage.py migrate
python manage.py createsuperuser --noinput || true
