#!/usr/bin/env bash
#sets up your web servers for the deployment of web_static.

apt-get update
apt-get install -y nginx

mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/


touch /data/web_static/releases/test/index.html
echo '
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
ubuntu@89-web-01:~/$ curl localhost/hbnb_static/index.html
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
' > /data/web_static/releases/test/index.html

ln -sf /data/web_static/releases/test/ /data/web_static/current

chown -R ubuntu:ubuntu /data/

echo '
server {
    listen 80 default_server;
    listen [::]:80 default_server;
    add_header X-Served-By $HOSTNAME;
    root   /var/www/html;
    index  index.html index.htm;

    location /hbnb_static {
	alias /data/web_static/current;
	index index.html index.htm;
    }

    rewrite ^/redirect_me https://www.mbumwa.com permanent;

    error_page 404 /custom_404.html;
    location = /custom_404.html {
      root /var/www/html;
      internal;
    }
}' > /etc/nginx/sites-available/default


service nginx restart
