export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
cd ~/selene
rm -rf selene
rm -rf static
rm -rf main
rm -rf manage.py
rm -rf requirements.txt
rm -rf templates
rm -rf apache2
rm -rf e.zip
unzip selene.zip
echo 'fin del unzip'
rm selene.zip
echo 'rm'
vagrant destroy -f
echo 'destroy'
vagrant up
echo 'up'
vagrant ssh
echo 'ssh'

