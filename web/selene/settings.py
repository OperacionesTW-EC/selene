"""
Django settings for selene project.

Generated by 'django-admin startproject' using Django 1.9.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.9/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOGIN_URL = "home"

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.9/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '5%#pk1c+=6o))6zf6ou01u!yf-mato-tk69fx%#a!ex6p@dyj&'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'main.apps.MainConfig',
    'devices.apps.DevicesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'pipeline',
    'jquery',
    'bootstrap3',
    'fontawesome',
    'django_nose',
    'rest_framework',
    'corsheaders'
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
]

ROOT_URLCONF = 'selene.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates', BASE_DIR+'/templates', '/vagrant/templates'],
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
WSGI_APPLICATION = 'selene.wsgi.application'

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


REST_FRAMEWORK = {
    'PAGE_SIZE': 10
}

# Internationalization
# https://docs.djangoproject.com/en/1.9/topics/i18n/

LANGUAGE_CODE = 'es-ES'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ['DB_NAME'],
        'USER': os.environ['DB_USER'],
        'PASSWORD': os.environ['DB_PASS'],
        'HOST': os.environ['DB_PORT_5432_TCP_ADDR'],
        'PORT': os.environ['DB_PORT_5432_TCP_PORT'],
    }
}

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'selene_test',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': 'db',
        'PORT': '5432',
    }

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.9/howto/static-files/

STATIC_URL = '/static/'
MEDIA_ROOT = '/media/'
MEDIA_URL = '/media/'
STATIC_ROOT = BASE_DIR+'/static/'

#PIPELINE

PIPELINE = {
    'STYLESHEETS': {

        'custom': {
            'source_filenames': (
                'css/custom.css',
            )
        },
    },
    'JAVASCRIPT': {
        'jquery': {
            'source_filenames': (
                'js/jquery.js',
            )
        },
        'bootstrap': {
            'source_filenames': (
                'twitter_bootstrap/js/transition.js',
                'twitter_bootstrap/js/modal.js',
                'twitter_bootstrap/js/dropdown.js',
                'twitter_bootstrap/js/scrollspy.js',
                'twitter_bootstrap/js/tab.js',
                'twitter_bootstrap/js/tooltip.js',
                'twitter_bootstrap/js/popover.js',
                'twitter_bootstrap/js/alert.js',
                'twitter_bootstrap/js/button.js',
                'twitter_bootstrap/js/collapse.js',
                'twitter_bootstrap/js/affix.js',
            ),
            'output_filename': 'js/b.js',
        },
    }
}

CORS_ORIGIN_ALLOW_ALL = True


STATICFILES_STORAGE = 'pipeline.storage.PipelineCachedStorage'

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'pipeline.finders.PipelineFinder',
)

TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'
