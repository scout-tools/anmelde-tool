import os
from datetime import timedelta
from pathlib import Path

import environ

env = environ.Env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# reading .env file
environ.Env.read_env()

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env('DEBUG')

ALLOWED_HOSTS = [
    '127.0.0.1',
    'localhost',
    'api.anmelde-tool.dev.scout-tools.de',
    'api.anmelde-tool.de',
]

CORS_ALLOW_CREDENTIALS = True

# Application definition

INSTALLED_APPS = [
    'rest_framework',
    'corsheaders',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'storages',
    'ebhealthcheck.apps.EBHealthCheckConfig',
    'django_extensions',
    'django_filters',
    'mozilla_django_oidc',
    'colorfield',
    'polymorphic',
    'basic',
    'authentication',
    'event',
    'inspi',
    'email_services',
    'drf_api_logger',
    'event.summary',
    'event.registration',
    'event.choices',
    'event.cash',
    'event.file_generator',
    'stdimage',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'mozilla_django_oidc.middleware.SessionRefresh',
    'drf_api_logger.middleware.api_logger_middleware.APILoggerMiddleware',
]

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates/emails/'),
        ],
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

WSGI_APPLICATION = 'backend.wsgi.application'

if env.bool('USE_RDS_DB'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': env('RDS_DB_NAME'),
            'USER': env('RDS_USERNAME'),
            'PASSWORD': env('RDS_PASSWORD'),
            'HOST': env('RDS_HOSTNAME'),
            'PORT': env('RDS_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': str(os.path.join(BASE_DIR, "db.sqlite3")),
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

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

LANGUAGE_CODE = 'de-de'

TIME_ZONE = 'Europe/Berlin'

USE_I18N = True

USE_L10N = True

USE_TZ = True

AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')

DRF_API_LOGGER_DATABASE = True

# https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/#private-media-files
# Continue tutorial for uploading images
if env.bool('USE_S3'):
    # aws settings
    AWS_S3_SIGNATURE_VERSION = 's3v4'
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'backend.storage_backends.StaticStorage'
    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'backend.storage_backends.PublicMediaStorage'
    # s3 private media settings
    PRIVATE_MEDIA_LOCATION = 'private'
    PRIVATE_FILE_STORAGE = 'backend.storage_backends.PrivateMediaStorage'
    PRIVATE_MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PRIVATE_MEDIA_LOCATION}/'
    AWS_S3_REGION_NAME = 'eu-central-1'
else:
    STATIC_URL = '/staticfiles/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_URL = '/mediafiles/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'mediafiles')

if env.bool('USE_S3_INSPI'):
    # aws settings
    AWS_ACCESS_KEY_ID = env('AWS_ACCESS_KEY_ID_INSPI')
    AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY_INSPI')
    AWS_STORAGE_BUCKET_NAME = env('AWS_STORAGE_BUCKET_NAME_INSPI')
    AWS_DEFAULT_ACL = 'public-read'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
    STATICFILES_STORAGE = 'backend.storage_backends.StaticStorage'
    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'media'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    DEFAULT_FILE_STORAGE = 'backend.storage_backends.PublicMediaStorage'

else:
    STATIC_URL = '/staticfiles/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    MEDIA_URL = '/inspi/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'inspi/media')

CORS_ORIGIN_WHITELIST = [
    "https://localhost:8000",
    "https://localhost:8080",
    "http://localhost:8000",
    "http://localhost:8080",
]

CORS_ORIGIN_ALLOW_ALL = True
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = True

SITE_ID = 1

SEND_MAIL = env.bool('USE_SES', False)

if SEND_MAIL:
    EMAIL_BACKEND = 'django_ses.SESBackend'
    AWS_SES_ACCESS_KEY_ID = env('AWS_SES_ACCESS_KEY_ID')
    AWS_SES_SECRET_ACCESS_KEY = env('AWS_SES_SECRET_ACCESS_KEY')
    AWS_SES_REGION_NAME = 'eu-central-1'
    AWS_SES_REGION_ENDPOINT = 'email.eu-central-1.amazonaws.com'
    EMAIL_HOST_USER = env('EMAIL_HOST_USER')
    FRONT_URL = env.str('FRONT_URL')

REST_USE_JWT = True

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'djangorestframework_camel_case.render.CamelCaseJSONRenderer',
        'djangorestframework_camel_case.render.CamelCaseBrowsableAPIRenderer',
    ),
    'DEFAULT_PARSER_CLASSES': (
        'djangorestframework_camel_case.parser.CamelCaseFormParser',
        'djangorestframework_camel_case.parser.CamelCaseMultiPartParser',
        'djangorestframework_camel_case.parser.CamelCaseJSONParser',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend'
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'mozilla_django_oidc.contrib.drf.OIDCAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}

AUTHENTICATION_BACKENDS = (
    'backend.OIDCAuthentication.MyOIDCAB',
    'django.contrib.auth.backends.ModelBackend',
)

BASE_URI = env('BASE_URI')
BASE_REALM_URI = f'{BASE_URI}realms/{env("OIDC_RP_REALMNAME")}'
OIDC_AUTH_URI = f'{BASE_REALM_URI}/{env("OIDC_RP_CLIENT_ID")}/'
OIDC_CALLBACK_PUBLIC_URI = f'{BASE_REALM_URI}/'
OIDC_RP_CLIENT_ID = env('OIDC_RP_CLIENT_ID')
OIDC_RP_CLIENT_SECRET = env('OIDC_RP_CLIENT_SECRET_BACKEND')
OIDC_OP_TOKEN_ENDPOINT = f'{BASE_REALM_URI}/protocol/openid-connect/token'
OIDC_OP_USER_ENDPOINT = f'{BASE_REALM_URI}/protocol/openid-connect/userinfo'
OIDC_OP_AUTHORIZATION_ENDPOINT = f'{BASE_REALM_URI}/protocol/openid-connect/auth'
OIDC_STORE_ID_TOKEN = True
OIDC_CREATE_USER = True

GRAPHENE = {
    "SCHEMA": "basic.schema.schema"
}

FILE_GENERATOR_DEQEUE_TIME = 60

from django.conf.global_settings import DATETIME_INPUT_FORMATS

DATETIME_INPUT_FORMATS += ('%Y-%m-%d %H:%M %p',)
