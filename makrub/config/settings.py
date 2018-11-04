"""
Django settings for makrub project.

Generated by 'django-admin startproject' using Django 2.0.2.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import sys
import os
import datetime
import dotenv
import requests

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

if os.environ.get('VAULT_TOKEN') is not None and os.environ.get('VAULT_TOKEN') != '':
    config_url = 'https://vault.studiotwist.co/v1/secret/data/makrub-%s/mkcore' % 'dev'
    res = requests.get(config_url, headers={"X-VAULT-TOKEN": os.environ['VAULT_TOKEN']})

    if res.status_code != 200:
        sys.exit('Error response %s: %s' % (res.status_code, res.text))

    config = res.json()['data']['data']['config']

    for c in config.splitlines():
        values = c.split('=')

        if len(values) == 2:
            os.environ[values[0]] = values[1]

else:
    dotenv_file = os.path.join(BASE_DIR, '.env')

    if os.path.isfile(dotenv_file):
        dotenv.read_dotenv(BASE_DIR)

    dotenv_file = os.path.join('/etc/app', '.env')

    if os.path.isfile('/etc/app/.env'):
        dotenv.read_dotenv('/etc/app')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', '%zmixicnvgn8gn)+ybg&%wx)fzk7oo3t4t#(wl2n*qzbk*vu23')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', False) == 'True'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'corsheaders',
    'rest_framework',
    'djoser',
    # 'django_otp',
    # 'django_otp.plugins.otp_totp',
    # 'django_otp.plugins.otp_static',

    'core',
    'api',
    'exporter',
    # 'otp',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

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

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASS'),
        'HOST': os.environ.get('DB_HOST'), # DB_HOST=172.17.0.1
        'PORT': os.environ.get('DB_PORT'), # DB_PORT=5432
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    # {
    #     'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    # },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 4,
        }
    },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    # },
    # {
    #     'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    # },
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-US'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# tell django to use my custom user model
AUTH_USER_MODEL = 'core.User'


# SMTP server for sending e-mail
# in development environment, do this:
# 1. python -m smtpd -n -c DebuggingServer localhost:1025
# 2. EMAIL_HOST = 'localhost'
# 3. EMAIL_PORT = 1025
# 4. delete other EMAIL_* configs in settings.py
EMAIL_HOST = os.environ.get('EMAIL_HOST')
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = os.environ.get('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_HOST_PASSWORD')
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'False').lower() == 'true'
# Set e-mail sender's name :
DEFAULT_FROM_EMAIL = 'Makrub.Com <no-reply@makrub.com>'


# auto append tailing slash to url
APPEND_SLASH = True


# CORS
# CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'localhost:3000',
    '127.0.0.1:3000',
    'localhost:8080',
    'dev.makrub.com',
    'dev-app.makrub.com',
    'mkcore-app.herokuapp.com',
)


######### django-rest-framework config :
# tell django rest framework that we're gonna use jwt for authen
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication', # JWT config
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}


######### django-rest-framework-jwt config:
JWT_AUTH = {
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=30),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=365),
    # 'JWT_GET_USER_SECRET_KEY': 'core.models.jwt_get_secret_key',
    # 'JWT_PAYLOAD_HANDLER': 'otp.utils.jwt_otp_payload',
}


######### WhiteNoise for serving static files
# Simplified static file serving.
# https://warehouse.python.org/project/whitenoise/
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

######### Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url

db_from_env = dj_database_url.config(conn_max_age=600)
DATABASES['default'].update(db_from_env)


######### djoser config:
DJOSER = {
    'PASSWORD_RESET_CONFIRM_URL': 'password/forgot/confirm/{uid}/{token}',
}
# django-templated-mail config (for djoser's e-mail content):
DOMAIN = os.environ.get('FRONTEND_DOMAIN', 'localhost:3000')
SITE_NAME = os.environ.get('FRONTEND_SITE_NAME', 'Localhost.me')


######### My custom variable for user activation e-mail content:
FRONTEND_APP_URL = os.environ.get('FRONTEND_APP_URL')


######### Facebook Settings
FACEBOOK_APP_ID = os.environ.get('FACEBOOK_APP_ID')
FACEBOOK_APP_SECRET = os.environ.get('FACEBOOK_APP_SECRET')
FACEBOOK_REDIRECT_URI = os.environ.get('FACEBOOK_REDIRECT_URI')
