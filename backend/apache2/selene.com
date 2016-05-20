<VirtualHost *:80>
        ServerName 10.0.0.25
        ServerAlias 10.0.0.25
        WSGIScriptAlias / /vagrant/selene/wsgi.py
        Alias /static/ /vagrant/static/
        <Directory /vagrant>
            Order allow,deny
            Allow from all
            </Directory>
            <Location "/static/">
                SetHandler None
            </Location>

</VirtualHost>