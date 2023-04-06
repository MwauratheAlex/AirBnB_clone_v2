#!/usr/bin/env bash
#sets up your web servers for the deployment of web_static.
#install nginx
apt-get update
apt-get install nginx

mkdir -p /data/
mkdir -p /data/web_static/
mkdir -p /data/web_static/releases/
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

NGINX_CONFIG="\\\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n"
sed -i '/server_name _;/a'"$NGINX_CONFIG" /etc/nginx/sites-available/default
service nginx restart
service nginx reload
