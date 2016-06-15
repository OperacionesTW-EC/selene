# selene
TW Selene Fixed Asset Backend

## Información

- Documentación y credenciales en Google Drive
- Trello: https://trello.com/b/UtxPAoUK/selene

## Tech Stack

- PostgreSQL (https://www.postgresql.org)
- Django (https://www.djangoproject.com)
- Django REST Framework (http://www.django-rest-framework.org)
- Python 3
- Test: nose (http://nose.readthedocs.io), Django REST Framework Test (http://www.django-rest-framework.org/api-guide/testing/)

## PostgreSQL en Mac

- Instalación:

  ```sh
  $ brew install postgresql
  $ initdb /usr/local/var/postgres -E utf8
  $ brew services start postgres
  ```

- Crear usuario/db postgres:

  ```sh
  $ psql postgres
  postgres=# create user postgres password 'postgres';
  postgres=# alter user postgres WITH SUPERUSER;
  postgres=# create database selene;
  postgres=#\q
  ```

- Cambiar método de autenticación a md5 en archivo `/usr/local/var/postgres/pg_hba.conf`.

## Python en Mac

- Instalación:

  ```sh
  $ brew install python python3
  $ pip install virtualenv
  ```

- Crear venv:

  ```sh
  $ virtualenv -p python3 seleneenv
  $ source seleneenv/bin/activate
  ```

- Salir del venv:

  ```sh
  $ deactivate
  ```

- Instalar dependencias (en la carpeta ```backend```, activar venv):

  ```sh
  $ pip install -r requirements.txt
  ```

## Iniciar aplicación:

- Variables de entorno:

  ```sh
  $ export DB_1_ENV_POSTGRES_DB=selene
  $ export DB_1_ENV_POSTGRES_USER=postgres
  $ export DB_1_ENV_POSTGRES_PASSWORD=postgres
  $ export DB_PORT_5432_TCP_ADDR=127.0.0.1
  $ export DB_PORT_5432_TCP_PORT=5432
  ```

- Ejecución de migraciones:

  ```sh
  $ ./manage.py migrate
  ```

- Ejecutar aplicación en desarrollo (en la carpeta ```backend```, activar venv):

  ```sh
  $ ./manage.py runserver
  ```

## Ejecución de pruebas

  ```sh
  $ ./manage.py test
  ```

## Creación de superuser para backoffice

  ```sh
  $ ./manage.py createsuperuser
  ```

## Estructura de carpetas

- **Archivos para producción**:

  Directorio ```backend/apache2```.

- **Pruebas E2E**:

  Directorio ```backend/e2e```.

- **Elementos Estáticos**:

  Directorio ```backend/static```.

- **Pruebas unitarias**:

  Usar la carpeta ```backend/devices/test``` para escribir las pruebas unitarias.

- **Rutas**:

  Usar el archivo ```backend/selene/urls.py```.

- **Configuraciones**:

  Usar el archivo ```backend/selene/settings.py```.
