"""
Django settings for easenso project.

Generated by 'django-admin startproject' using Django 1.8.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

BASE_DIR      = os.path.dirname(os.path.dirname(__file__))

TEMPLATE_PATH = os.path.join(BASE_DIR, 'templates')

STATIC_PATH   = os.path.join(BASE_DIR, 'static')

MEDIA_PATH    = os.path.join(BASE_DIR, 'media')


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'uh*2bl%q#94efo#5t&)xovu1a$d(k&9z$2w)(oftu8+rajsmov'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = DEBUG

ALLOWED_HOSTS = [ '127.0.0.1']

SESSION_EXPIRE_AT_BROWSER_CLOSE = True

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'top.easenso@gmail.com'
EMAIL_HOST_PASSWORD = 'saltopso24'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# Application definition
SESSION_COOKIE_DOMAIN = 'localhost'

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'easenso',
    'users',
    'product',
    'business',
    'captcha',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'easenso.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_PATH.replace('\\','/')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.core.context_processors.i18n',
                'django.core.context_processors.media',
                'django.core.context_processors.static',
                'django.core.context_processors.tz',
            ],
        },
    },
]

WSGI_APPLICATION = 'easenso.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.postgresql_psycopg2',
        'NAME'     : 'easenso_database',
        'USER'     : 'postgres',
        'PASSWORD' : 'postgres',
        'HOST'     : 'localhost',
        'PORT'     : '5432',
    }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_ROOT = ''

STATIC_URL = '/static/'

STATICFILES_DIRS = ( STATIC_PATH.replace('\\','/'),
)

STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_ROOT = MEDIA_PATH

MEDIA_URL = '/media/'

AUTH_USER_MODEL = "users.User"