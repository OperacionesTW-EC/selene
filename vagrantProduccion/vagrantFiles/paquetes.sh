#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install -y software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get -y install ansible
sudo apt-get -y install python-pip
sudo apt-get -y install libpq-dev
sudo apt-get -y install python-dev
sudo apt-get -y install apache2
sudo apt-get -y install apache2-dev
sudo apt-get install libapache2-mod-wsgi
