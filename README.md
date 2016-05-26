# Selene
## Version
0.1

## Antecedente
El presente documento te ayudará a levantar los ambientes de GO CD, QA y Producción, además, de dar una introducción de los comandos más usados para la arquitectura seleccionada.


## PostgreSQL en mac
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

- Cambiar de método de autenticación a md5 en archivo `/usr/local/var/postgres/pg_hba.conf`

## Python en mac

- Instalación:
  ```sh
  $ brew install python
  $ pip install --upgrade setuptools
  $ pip install --upgrade pip
  $ pip install virtualenv
  ```

- Crear venv:
  ```sh
  $ virtualenv seleneenv
  $ source seleneenv/bin/activate
  $ pip install -r requirements.txt
  ```

- Salir del venv:
  ```sh
  $ deactivate
  ```

- Iniciar aplicación:
  ```sh
  #!/bin/bash
  export DB_1_ENV_POSTGRES_DB=selene
  export DB_1_ENV_POSTGRES_USER=postgres
  export DB_1_ENV_POSTGRES_PASSWORD=postgres
  export DB_PORT_5432_TCP_ADDR=127.0.0.1
  export DB_PORT_5432_TCP_PORT=5432
  python manage.py runserver 0.0.0.0:8000
  ```

## TODO
- [ ] Ilustración de última arquitectura
- [ ] Diagrama de componentes
- [ ] Comandos intalación de python en mac
- [ ] Usar local-docker.sh

[docker-toolbox]: (https://www.docker.com/products/docker-toolbox/)
