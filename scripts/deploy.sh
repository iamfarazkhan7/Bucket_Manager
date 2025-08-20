# File: scripts/deploy.sh
#!/bin/bash

# Production deployment script
set -e

echo "Starting deployment..."

# Wait for database to be ready (for Docker)
if [ "$DATABASE_URL" != "" ]; then
    echo "Waiting for database..."
    python -c "
import time
import psycopg
import os
from urllib.parse import urlparse

max_retries = 30
retry_count = 0

while retry_count < max_retries:
    try:
        db_url = os.getenv('DATABASE_URL')
        if db_url and 'postgresql' in db_url:
            parsed = urlparse(db_url)
            conn = psycopg.connect(
                host=parsed.hostname,
                port=parsed.port,
                user=parsed.username,
                password=parsed.password,
                dbname=parsed.path[1:]
            )
            conn.close()
            print('Database is ready!')
            break
    except Exception as e:
        retry_count += 1
        print(f'Database not ready yet... ({retry_count}/{max_retries})')
        time.sleep(2)
else:
    print('Could not connect to database after maximum retries')
    exit(1)
"
fi

# Run migrations
echo "Running migrations..."
python manage.py migrate --noinput

# Create superuser if environment variables are set
echo "Setting up admin user..."
python manage.py shell -c "
from django.contrib.auth.models import User
import os

username = os.getenv('ADMIN_USER')
email = os.getenv('ADMIN_EMAIL')
password = os.getenv('ADMIN_PASSWORD')

if username and email and password:
    if not User.objects.filter(username=username).exists():
        User.objects.create_superuser(username, email, password)
        print(f'Superuser {username} created successfully!')
    else:
        print(f'Superuser {username} already exists.')
else:
    print('Admin environment variables not set, skipping superuser creation.')
"

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn server..."
exec gunicorn bucket_manager.wsgi:application \
    --bind 0.0.0.0:8000 \
    --workers 3 \
    --worker-class sync \
    --worker-connections 1000 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --timeout 30 \
    --keep-alive 5 \
    --log-level info \
    --access-logfile - \
    --error-logfile -