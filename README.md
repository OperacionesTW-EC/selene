# Selene
## Version
0.1

## Antecedente
El presente documento te ayudará a levantar los ambientes de GO CD, QA y Producción, además, de dar una introducción de los comandos más usados para la arquitectura seleccionada.

## Usando Docker
Guía de instalación con Docker para Mac
- Instalar [docker-toolbox]:

  ```sh
  $ brew cask install dockertoolbox
  ```

- Para crear la máquina, ejecutar el comando:

  ```sh
  $ docker-machine create --driver virtualbox default
  ```

  Nota: El último argumento es el nombre de la máquina

- Para conectarse con la nueva máquina, ejecutar el comando:

  ```sh
  $ eval "$(docker-machine env default)"
  ```

  Nota: Ejecutar antes para usos posteriores de docker.

- Ejecutar el contenedor con el comando:

  ```sh
  $ docker-compose -f docker-compose.devel.yml up
  ```

### Comandos de ayuda
- Iniciar máquina:

  ```sh
  $ docker-machine start default
  ```

  Nota: Se debe ejecutar si se muestra el siguiente mensaje "Error checking TLS connection: Host is not running"

- Mostrar el listado de máquinas:

  ```sh
  $ docker-machine ls
  ```

- Obtener el IP de la máquina:​

  ```sh
  $ docker-machine ip default
  ```

## Comandos Git Submodule
- Luego de clonar el proyecto:

  ```sh
  $ git submodule init
  ```

- Actualizar submodules:

  ```sh
  $ git submodule update
  ```

  Nota: Si no se tiene acceso al submodule `config`, se puede actualizar solo ui:  git submodule update ui

- Importante moverse a branch master en submodule:

  ```sh
  $ cd ui
  $ git checkout master
  ```

## NPM
- Instalar node y nvm:

  ```sh
  $ brew install node
  $ npm install -g nvm
  ```

  Verificar la versión instalada:

  ```sh
  $ node --version
  ```

- Descargar e instalar la versión de NVM

  ```sh
  $ nvm download 4.4.4
  $ nvm build 4.4.4
  $ nvm install 4.4.4
  ```

- Instalar las dependencias de nuestra aplicación. Dentro del directorio `ui` ejecutar:

  ```sh
  $ npm install
  ```

- Iniciar aplicación:
  ```sh
  $ npm start
  ```

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
