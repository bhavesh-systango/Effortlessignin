"""
Django settings for effortles project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path
import os
from decouple import config

BASE_DIR = Path(__file__).resolve().parent.parent


SECRET_KEY = config('SECRET_KEY')


DEBUG = config('DEBUG_STATE')


ALLOWED_HOSTS = ['*']
CSRF_TRUSTED_ORIGINS = ['https://35.238.228.25']


INSTALLED_APPS = [
    'authentication',
    'employee',
    'attendance',
    'feed',
    'event',

    'rest_framework',
    'rest_framework_simplejwt',
    'django_filters',
    'django_celery_results',
    'django_celery_beat',
    'debug_toolbar',
    'kronos',
    
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = 'effortles.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


WSGI_APPLICATION = 'effortles.wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'), 
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'), 
        'PORT': config('DB_PORT'),
    }
}


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTH_USER_MODEL = "authentication.User"


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATICFILES_DIRS= [
    os.path.join(BASE_DIR, "authentication/assets"),
    os.path.join(BASE_DIR, "employee/assets"),
    os.path.join(BASE_DIR, "attendance/assets"),
]
STATIC_ROOT = os.path.join(BASE_DIR, "static")


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = '/authentication/dashboard'


EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"


LOGIN_URL = '/authentication/login'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ]
}

EMAIL_HOST = "localhost"
EMAIL_PORT = "1025"
EMAIL_HOST_USER = ""
EMAIL_HOST_PASSWORD = ""
EMAIL_USE_TLS = False


# celery setting
CELERY_BROKER_URL = config('CELERY_BROKER_URL')
# CELERY_RESULT_BACKEND = 'redis://127.0.0.1:6379'
CELERY_RESULT_BACKEND = 'django-db'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Asia/Kolkata'

# celery beat
CELERY_BEAT_SCHEDULAR = 'django_celery_beat_schedulers:DataBaseSchedular'


INTERNAL_IPS = [
    "127.0.0.1",
]


if DEBUG:
    STRIPE_PUBLISHABLE_KEY = 'pk_test_51LBCYJSBF1HSCN9I3C4JzyO4qrYKY6gdc77zlwMHfzNqfLtVrTxNxaMxKpDnrgiOm3VycSN5sunlNCpYSjsf7IN700M4mU9gLZ'
    STRIPE_SECRET_KEY = 'sk_test_51LBCYJSBF1HSCN9IKm1Fg6LfiJrrCgmHz2lkkd9eJTYvrSz0wuUWeHpMONKYIUMjqzrtQG2ZhiP206YT9sb9sW0a00vd5JHygv'