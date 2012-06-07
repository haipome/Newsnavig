<VirtualHost *:80>

    ServerName nng.com
    RedirectMatch permanent ^/(.*) http://www.nng.com/$1

</VirtualHost>

<VirtualHost *:80>

    ServerName www.nng.com
    DocumentRoot /home/haipo/nng

    <Directory /home/haipo/nng>
        Options FollowSymLinks
        AllowOverride None
        Order allow,deny
        Allow from all
    </Directory>

    Alias /favicon.ico /home/haipo/nng/media/favicon.ico
    Alias /robots.txt /home/haipo/nng/static/robots.txt

    WSGIScriptAlias / /home/haipo/nng/nng/wsgi.py

    Alias /static/ /home/haipo/nng/static/
    <Location "/static/">
        SetHandler None
    </Location>

    Alias /media/ /home/haipo/nng/media/
    <Location "/media/">
        SetHandler None
    </Location>

    <LocationMatch "(?i)\.(jpg|gif|png|txt|ico|css|js)$">
       SetHandler None
    </LocationMatch>

</VirtualHost>

<VirtualHost *:80>

    ServerName static.nng.com
    
    Alias / /home/haipo/nng/static/
    <Location "/">
        Options FollowSymLinks
        SetHandler None
    </Location>

</VirtualHost>

<VirtualHost *:80>

    ServerName media.nng.com
    
    Alias / /home/haipo/nng/media/
    <Location "/">
        Options FollowSymLinks
        SetHandler None
    </Location>

</VirtualHost>
