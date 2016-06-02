export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
source /home/selene/.bash_profile
rm -rf /home/selene/backend
tar -xvf /home/selene/selene_backend.tar -C /home/selene
rm -rf /home/selene/selene_backend.tar
cd /home/selene/backend
export DEVICE_FILE_PATH=/home/selene/migrationFiles/devices.csv
pip3 install -r requirements.txt
yes | ./manage.py migrate
chown -R selene:selene /home/selene/backend
systemctl restart httpd
