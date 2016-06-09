# Selene Full-Stack End-to-End Tests

## Dependencias de Lettuce
* No supporta python 3 por su usa del 'print foo' sin paréntesis
* Por tanto usa el python 2 más reciente (2.7.11 al momento) en un
  entorno virtual aparte de lo de la appliación

## Python en mac

- Instalación:
  ```sh
  $ brew install python  # 2.7.11 o más alta
  $ pip install --upgrade setuptools
  $ pip install --upgrade pip
  $ pip install virtualenv
  ```

- Crear venv para e2e:
  ```sh
  # en dir 'selene'
  $ python --version  # debería ser 2.7.xx
  $ virtualenv ../py2-selene
  $ source ../py2-selene/bin/activate
  $ pip install -r backend/e2e/e2e-requirements.txt
  ```

- Salir del venv:
  ```sh
  $ deactivate
  ```

- correr pruebas:
  ```sh
  $ cd backend/e2e
  $ lettuce
  ```

