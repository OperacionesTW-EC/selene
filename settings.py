DATABASES = {
    default: {
        ENGINE: 'django.db.backends.postgresql_psycopg2',
        NAME: selene,
        USER: postgres,
        PASSWORD: postgres,
        HOST: db,
        PORT: 5432,
    }
}
