#!/bin/bash

# Install Python dependencies
pip install --no-cache-dir -r requirements.txt

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate 