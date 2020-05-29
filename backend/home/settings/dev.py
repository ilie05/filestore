"""Use this for development"""

from .base import *

# ALLOWED_HOSTS += ['127.0.0.1', 'http://ec2-54-211-123-16.compute-1.amazonaws.com']
ALLOWED_HOSTS += ['*']
DEBUG = True

WSGI_APPLICATION = 'home.wsgi.dev.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',
)
