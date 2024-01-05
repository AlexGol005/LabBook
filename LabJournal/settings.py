"""
Django settings for LabJournal project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

#
# SECRET_KEY = "vs3umg+heg!)ljfeg2o^eu@3fk1ma!=ett2^9o2x8cwjl@0ixy"
# DEBUG = True
# ALLOWED_HOSTS = []




EMAIL_HOST = 'smtp.mail.ru'
EMAIL_PORT = 465
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
EMAIL_HOST_USER = 'sandra.005@mail.ru'
SERVER_EMAIL = 'sandra.005@mail.ru'
DEFAULT_FROM_EMAIL = 'sandra.005@mail.ru'
EMAIL_HOST_PASSWORD = '7B7YUqnEHbTgT6iDtJey'

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG') == "true"

ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS').split(',')]

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'viscosimeters',
    'kinematicviscosity',
    'users.apps.UsersConfig',
    'rest_framework',
    'crispy_forms',
    'equipment',
    'jouViscosity',
    'dinamicviscosity',
    'blog',
    'bdanswers',
    'contact_form',
    # 'ckeditor',
    # 'ckeditor_uploader',
]



CRISPY_TEMPLATE_PACK = 'bootstrap4'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'LabJournal.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates']
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'main.context_processors.base_context.last_news',
                'main.context_processors.base_context.last_ad',
                'main.context_processors.base_context.USER',
            ],
        },
    },
]

WSGI_APPLICATION = 'LabJournal.wsgi.application'

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True

USE_L10N = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_DIR = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [STATIC_DIR]
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_REDIRECT_URL = 'profile'
LOGIN_URL = 'user'

MEDIA_URL = '/pictures/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'pictures')

SHORT_DATE_FORMAT = 'j . m. Y'

TOOLBAR_DEBUG = False

if TOOLBAR_DEBUG:
    try:
        from LabJournal import local_settings

        INSTALLED_APPS += local_settings.INSTALLED_APPS
        MIDDLEWARE = local_settings.MIDDLEWARE + MIDDLEWARE

        INTERNAL_IPS = local_settings.INTERNAL_IPS
    except ImportError as e:
        import logging

        logger = logging.getLogger(__name__)
        logger.warning(f"Ошибка импорта. {e}")

if DEBUG:
    import mimetypes

    mimetypes.add_type("application/javascript", ".js", True)



