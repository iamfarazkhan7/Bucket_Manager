# File: scripts/dev.sh
#!/bin/bash

# Development script
set -e

echo "Setting up development environment..."

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating .env file from .env.example..."
    cp .env.example .env
fi

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "Running migrations..."
python manage.py makemigrations
python manage.py migrate

# Create superuser if it doesn't exist
echo "Setting up admin user..."
python manage.py shell -c "
from django.contrib.auth.models import User
import os

username = os.getenv('ADMIN_USER', 'admin')
email = os.getenv('ADMIN_EMAIL', 'admin@example.com')
password = os.getenv('ADMIN_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created successfully!')
else:
    print(f'Superuser {username} already exists.')
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Run development server
echo "Starting development server..."
python manage.py runserver 0.0.0.0:8000