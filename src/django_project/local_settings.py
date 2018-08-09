DEBUG = True

SECRET_KEY = 'super-secure-hash'

# -----------------
# STATIC & MEDIA
# -----------------

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/vagrant/webapp/src/backend/src/media'
STATIC_URL = '/static/'
STATIC_ROOT = '/home/vagrant/webapp/src/backend/src/collected_static'


# -----------------
# Database
# -----------------

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'django_app',
        'USER': 'django_app',
        'PASSWORD': 'qwe123',
        'HOST': 'localhost',
        'PORT': 5432,
        'TEST': {
            'NAME': 'django_app_test_db',
        }
    }
}


# -----------------
# Cache
# -----------------

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': 'redis://127.0.0.1:6379/1',
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'PARSER_CLASS': 'redis.connection.HiredisParser',
        }
    }
}


# -----------------
# CHANNELS
# -----------------

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("redis_6379", 6379)],
        },
    },
}


# -----------------
# Celery
# -----------------

BROKER_URL = 'redis://127.0.0.1:6379/2'
CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379/3'


# -----------------
# Project
# -----------------

SITE_URL = 'http://webapp.local'
API_URL = 'http://api.webapp.local'

