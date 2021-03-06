"""
Django settings for mini_blog project.

Generated by 'django-admin startproject' using Django 3.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import ast
from django.utils.translation import ugettext_lazy as _
from dotenv import load_dotenv
from pathlib import Path

# Loading environment variables
env = Path(__file__).parent.parent.joinpath('.env')
load_dotenv(env)

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ast.literal_eval(os.environ.get('DEBUG'))

ALLOWED_HOSTS = ['*']

# DEBUG_PROPAGATE_EXCEPTIONS = True


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'blog.apps.BlogConfig',
    'users.apps.UsersConfig',
    'widget_tweaks',
    'ckeditor',
    # Login with Google
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',
    # Django toolbar
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    # Django toolbar
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'mini_blog.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'mini_blog.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
	'ENGINE': os.environ.get('ENGINE', default='django.db.backends.sqlite3'),
        'NAME': os.environ.get('DB_NAME', os.path.join(BASE_DIR, 'db.sqlite3'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST'),
        'PORT': int(os.environ.get('DB_PORT')),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# For Login
LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'user:sign-in'

# Celery
CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL')
CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND')
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_AMQP_TASK_RESULT_EXPIRES = 1000


# Do not use https on localhost
if not ast.literal_eval(os.environ.get('LOCAL')):
    CSRF_COOKIE_SECURE = True
    SECURE_SSL_REDIRECT = True

# Correct styles on Heroku
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

FIXTURE_DIRS = (
   os.path.join(STATIC_ROOT, 'fixtures'),
)

# Media
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'

# ckeditor settings
CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': [
            [
                'Undo', 'Redo',
                '-', 'Bold', 'Italic', 'Underline', 'Strike', 'Subscript',
                '-', 'Link', 'Unlink', 'Anchor',
                '-', 'Format', 'Styles',
                '-', 'Maximize',
                '-', 'Table',
                '-', 'Image',
                '-', 'NumberedList', 'BulletedList', 'RemoveFormat'
            ],
            ['Find'],
            ['Replace', 'SelectAll'],
            ['Maximize'],
            ['Flash'],
            ['Smiley'],
            [
                'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock',
                '-', 'Font', 'FontSize', 'TextColor', 'BGColor',
                '-', 'Outdent', 'Indent',
                '-', 'HorizontalRule',
                '-', 'Blockquote',
            ],
            ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord'],
            ['SpecialChar', 'ShowBlocks'],
            ['Source'],
            ['BidiLtr', 'BidiRtl'],
        ],
        'height': '400',
        'width': '100%',
        'toolbarCanCollapse': False,
        'forcePasteAsPlainText': True,
    },
}

SITE_ID = 1

# Social accounts (username and email required)
ACCOUNT_USERNAME_REQUIRED = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
# Timeout: 1 day
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 86400


# Translations
LANGUAGES = (
    ('en', _('English')),
    ('ru', _('Russian')),
    ('uk', _('Ukrainian')),
)

LANGUAGE_CODE = 'en'

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)

# 403 error handler
CSRF_FAILURE_VIEW = 'blog.views.csrf_failure'

# Django toolbar (only for localhost)
INTERNAL_IPS = [
    '127.0.0.1',
]
