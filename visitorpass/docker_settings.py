"""
Docker-specific Django settings for visitorpass project.
"""

from .settings import *

# Static files configuration for Docker
STATIC_URL = '/static/'
STATIC_ROOT = '/app/static'
STATICFILES_DIRS = []  # Clear any STATICFILES_DIRS to avoid conflicts

# Media files configuration for Docker
MEDIA_URL = '/media/'
MEDIA_ROOT = '/app/media'

# Debug settings
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Security settings
SECRET_KEY = os.environ.get('SECRET_KEY', SECRET_KEY)
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')

# Database configuration
DATABASE_URL = os.environ.get('DATABASE_URL')
if DATABASE_URL:
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL)
    }
elif os.environ.get('USE_SQLITE', 'False') == 'True':
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
