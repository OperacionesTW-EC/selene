tput setaf 1;
echo '--------------bajando el servidor------------------------------'
tput sgr0;
sudo /etc/init.d/apache2 stop
tput setaf 1;
echo '--------------borrando versiones anteriores--------------------'
tput sgr0;
sudo rm /etc/apache2/sites-available/*
sudo rm /etc/apache2/sites-enabled/*
sudo a2dissite selene.com
tput setaf 1;
echo '--------------copiando archivo selene.com----------------------'
tput sgr0;
sudo cp selene.com /etc/apache2/sites-available/
tput setaf 1;
echo '--------------activando sitio----------------------------------'
tput sgr0;
sudo a2ensite selene.com
tput setaf 1;
echo '--------------Suebiendo el servidor----------------------------'
tput sgr0;
sudo /etc/init.d/apache2 start