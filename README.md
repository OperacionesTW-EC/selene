# Selene


### Version
0.1

### Antecedente
El presente documento te ayudará a levantar los ambientes de GO CD, QA y Producción

### Requisitos de la maquina donde se quiere levantar los ambientes
* [Vagrant] - version 1.8.0
* [VirtualBox] - version 5.0.12
* [vagrant-triggers]

### Usando Docker

Guía de instalación con Docker para Mac

* Instalar [docker toolbox]: <https://www.docker.com/products/docker-toolbox>
* Para crear la máquina, ejecutar el comando: 
```sh
  $ docker-machine create --driver virtualbox default
```

  Nota: El último argumento es el nombre de la máquina 
  Para conectarse con la nueva máquina, ejecutar el comando:
  eval "$(docker-machine env default)"
  
* Ejecutar el contenedor con el comando:
```sh
  $ docker-compose up
```
Comandos de ayuda:

Mostrar el listado de máquinas:
```sh
  $ docker-machine ls
```
Obtener el IP de la máquina:​
```sh
  $ docker-machine ip default
```
Conectarse:
```sh
  $ docker run -it busybox sh
```
Referencia: https://docs.docker.com/machine/get-started/ 


### Crear GO CD 
Revisar README de la carpeta gocd
### Crear Producción
De la carpeta vagrantProduccion copiar los documentos 
* file Vagrantfile
* file settings_produccion
* folder vagrantfiles
A la carpeta /usr/your_user/selene

### Crear QA
De la carpeta vagrantProduccion copiar los documentos 
* file Vagrantfile
* file settings_qa
* folder vagrantfiles
A la carpeta /usr/your_user/selene

### Contenido de maquina QA y Produccion

Las maquinas virtuales estan instalada con las siguientes características:

* [Ubuntu]- distribución 
* [Python]- version 2.7
* [Pip]
* [zip]
* [unzip]
* [apache2]




**Suerte!**

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

  [Ubuntu]: <http://www.ubuntu.com/>
   [Java]: <http://openjdk.java.net/install/>
   [Python]: <https://www.python.org/>
   [Pip]: <https://pypi.python.org/pypi/pip> 
   [Go server]:<https://www.go.cd/>
   [Go agent]:<https://www.go.cd/>
   [Vagrant]:<https://www.vagrantup.com/>
   [VirtualBox]:<https://www.virtualbox.org/>
   [git]:<https://git-scm.com/> 
   [zip]:<http://packages.ubuntu.com/precise/zip> 
   [unzip]:<http://packages.ubuntu.com/precise/unzip> 
   [apache2]:<https://help.ubuntu.com/lts/serverguide/httpd.html> 
   [vagrant-triggers]: <https://github.com/emyl/vagrant-triggers>



