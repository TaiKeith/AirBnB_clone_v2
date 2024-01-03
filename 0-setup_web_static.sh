#!/usr/bin/env bash
# This script sets up my web servers for the deployment of web_static
sudo apt-get update
sudo apt-get install -y nginx

sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" >> /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /data/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

sudo sed -i '/server {/a \\n    location /hbnb_static {\n\talias /data/web_static/current/;\n    }\n' /etc/nginx/sites-available/default

service nginx restart
