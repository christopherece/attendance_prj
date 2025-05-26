FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    pip install --no-cache-dir dj-database-url

# Copy project files
COPY . .

# Create entrypoint script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Run migrations\n\
python manage.py migrate\n\
\n\
# Create superuser\n\
python manage.py shell -c "\
from django.contrib.auth.models import User; \
import os; \
username = os.environ.get(\"ADMIN_USERNAME\", \"admsrv\"); \
password = os.environ.get(\"ADMIN_PASSWORD\", \"adminpass\"); \
email = os.environ.get(\"ADMIN_EMAIL\", \"admin@example.com\"); \
User.objects.filter(username=username).exists() or User.objects.create_superuser(username, email, password); \
print(f\"Admin user {username} is ready to use.\")\
"\n\
\n\
# Start server\n\
exec "$@"' > /entrypoint.sh && chmod +x /entrypoint.sh

# Expose port
EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
