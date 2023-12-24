#!/usr/bin/env bash
# This script sets up my web servers for the deployment of web_static
apt-get update
apt-get install -y nginx

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /dada/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

sed -i '/server {/a \\n    location /hbnb_static {\n\talias /data/web_static/current/;\n    }\n' /etc/nginx/sites-available/default

service nginx restart
