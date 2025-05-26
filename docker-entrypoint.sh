#!/bin/bash

set -e

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files with proper permissions
echo "Collecting static files..."
python manage.py collectstatic --noinput
# Ensure static files are accessible
find /app/static -type d -exec chmod 755 {} \;
find /app/static -type f -exec chmod 644 {} \;

# Create default admin user
echo "Creating default admin user..."
python manage.py shell <<EOF
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
try:
    if not User.objects.filter(username='admsrv').exists():
        User.objects.create_superuser('admsrv', 'admin@example.com', 'adminpass')
        print("Default admin user created successfully")
    else:
        print("Admin user already exists")
except IntegrityError:
    print("Admin user already exists")
EOF

# Start server
echo "Starting server..."
exec "$@"
