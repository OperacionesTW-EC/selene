import dj_database_url
import sys

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'selene',
        'USER': 'postgres',
        'PASSWORD': 'postgres',
        'HOST': '10.71.23.242',
        'PORT': '5432',
    }
}