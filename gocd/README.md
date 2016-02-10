# GO CD para Selene

### Version
0.1

### Características

La maquina virtual de GO CD esta instalada con las siguientes características:

* [Ubuntu]- distribución 
* [Java]- version 1.7.0_95
* [Python]- version 2.7
* [Pip]
* [Go server] - version 16
* [Go agent] - version 16
* [git]
* [zip]
* [unzip]

### Requisitos
* [Vagrant] - version 1.8.0
* [VirtualBox] - version 5.0.12
* [git]

### Instalación

Para poder levantar el GO CD , primero debes , clonar el repositorio de Selene y copiar la carpeta gocd al lugar donde se desee crear la vm con GO CD 
```sh
$ git clone https://veronica_rodriguez@bitbucket.org/valentinsvt/selene.git
$ cd selene/gocd/
$ cp gocd <your path>
```
Luego, ya dentro de la carpeta gocd ejecutamos
```sh
$ vagrant plugin install vagrant-triggers
$ vagrant up
$ vagrant ssh
```
Finalmente creamos debemos crear el pipeline de Selene

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


