#!/bin/bash

# Exit on error
set -e

# Install system dependencies
echo "Installing system dependencies..."
apt-get update
apt-get install -y libpq-dev python3-dev

# Create and activate virtual environment
echo "Setting up Python environment..."
python -m venv venv
source venv/bin/activate

# Upgrade pip and install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Build completed successfully!" 