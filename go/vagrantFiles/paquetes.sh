#!/usr/bin/env bash





  echo "--------------------------Update and add repository--------------------------------"
 
  sudo apt-get update
  #Now, install python-software-properties so we have the "add-apt-repository" command available
  sudo apt-get -y install python-software-properties
  sudo add-apt-repository ppa:rquillo/ansible
  #Now we run this again so that we get the very latest version of ansible's repository
  sudo apt-get update
  #finally, install ansible
  sudo apt-get -y install ansible

  echo "--------------------------Installing python--------------------------------"
  sudo apt-get -y install python-pip
  sudo apt-get -y install libpq-dev
  sudo apt-get install python-dev -y
  #sudo apt-get update
  echo "--------------------------Installing java--------------------------------"
  sudo apt-get install -y openjdk-7-jre

  echo "----------------------------Download GO CD server and Agent----------------"

  echo "Dowloading and installing GO CD server"
  echo "deb http://dl.bintray.com/gocd/gocd-deb/ /" > /etc/apt/sources.list.d/gocd.list
  wget --quiet -O - "https://bintray.com/user/downloadSubjectPublicKey?username=gocd" | sudo apt-key add -
  echo "deb http://dl.bintray.com/gocd/gocd-deb/ /" | sudo tee -a /etc/apt/sources.list.d/gocd.list
  wget --quiet -O - "https://bintray.com/user/downloadSubjectPublicKey?username=gocd" | sudo apt-key add -
  
  echo "------------------------------Update repository-----------------------"
  apt-get update

  echo "------------------------------Installing GO CD Server-----------------------"
  apt-get -y install go-server
  sudo service go-server start

  echo "------------------------------Installing GO CD Agent-------------------------"
  
  sudo apt-get install go-agent
  sudo service go-agent start

