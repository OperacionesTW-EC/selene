export PATH=/usr/bin:/bin:/usr/sbin:/sbin:/usr/local/bin
source /home/$USER/.bash_profile
rm -rf /home/$USER/backend
tar -xvf /home/$USER/selene_backend.tar -C /home/$USER
rm -rf /home/$USER/selene_backend.tar
cd /home/$USER/backend
export DEVICE_FILE_PATH=/home/$USER/migrationFiles/devices.csv
sudo pip3 install -r requirements.txt
yes | ./manage.py migrate
chown -R $USER:$USER /home/$USER/backend
sudo systemctl restart $SERVICE_NAME
