"""
Django settings for devoted_heart project.

Generated by 'django-admin startproject' using Django 5.0.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""
import os
from pathlib import Path
from datetime import timedelta

from dotenv import load_dotenv

from core.constants import (
    JWT_TOKEN_FILE_DAYS, DEFAULT_PAGE_SIZE
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_DIR = 'database'


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

load_dotenv()
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', 'no_secrets_from_us')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv('DEBUG', '').lower() == 'true' else False

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
MAIN_HOST = os.getenv('MAIN_HOST', None)
if MAIN_HOST is not None:
    ALLOWED_HOSTS.append(MAIN_HOST)


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'django_object_actions',
    'djoser',
    'import_export',
    'rangefilter',
    'users',
    'app',
    'api',
    'drf_yasg',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'devoted_heart.urls'

STATIC_ROOT = BASE_DIR / 'collected_static'

MEDIA_ROOT = '/media/'

MEDIA_URL = '/media/'

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

WSGI_APPLICATION = 'devoted_heart.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / DATABASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

PASSWORD_VALIDATION = 'django.contrib.auth.password_validation'
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': f'{PASSWORD_VALIDATION}.UserAttributeSimilarityValidator',
    },
    {
        'NAME': f'{PASSWORD_VALIDATION}.MinimumLengthValidator',
    },
    {
        'NAME': f'{PASSWORD_VALIDATION}.CommonPasswordValidator',
    },
    {
        'NAME': f'{PASSWORD_VALIDATION}.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_PAGINATION_CLASS':
        'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': DEFAULT_PAGE_SIZE,
}

SIMPLE_JWT = {
   'ACCESS_TOKEN_LIFETIME': timedelta(days=JWT_TOKEN_FILE_DAYS),
   'AUTH_HEADER_TYPES': ('Token',),
}

DJOSER = {
    'LOGIN_FIELD': 'email',
}
