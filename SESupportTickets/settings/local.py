import os
from .base import *


# Create necessary directories
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

DEBUG = True
SECRET_KEY = 'django-insecure-^i8p1d+yc6^%e4bl#-*tk!@^r(juy=q-3-)y9_60(b+g$eo&3-'
ALLOWED_HOSTS = ['localhost', '127.0.0.1']

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'tickets',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Disable security settings in development
SECURE_SSL_REDIRECT = False
CSRF_COOKIE_SECURE = False
SESSION_COOKIE_SECURE = False

# Debug toolbar settings
INTERNAL_IPS = ['127.0.0.1']

# Local logging configuration
LOGGING['handlers']['file'] = {
    'level': 'INFO',
    'class': 'logging.FileHandler',
    'filename': LOGS_DIR / 'django.log',
    'formatter': 'verbose',
}
LOGGING['root']['handlers'].append('file')

# DRF settings for development
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
]