import dj_database_url
import sys

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'selene',
        'USER': 'postgres',
        'PASSWORD': '!selene_playa',
        'HOST': '10.71.23.241',
        'PORT': '5432',
    }
}