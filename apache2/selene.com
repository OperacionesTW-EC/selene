<VirtualHost *:80>
        ServerName 10.0.0.25
        ServerAlias 10.0.0.25
        WSGIScriptAlias / /vagrant/selene/wsgi.py
        Alias /static/ /vagrant/selene/static/
        <Location "/static/">
            Options -Indexes
        </Location>
</VirtualHost>