export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
rm -rf /home/selene/backend
tar -xvf /home/selene/selene_backend.tar -C /home/selene
rm -rf /home/selene/selene_backend.tar
cd /home/selene/backend/apache2
sudo systemctl restart httpd
