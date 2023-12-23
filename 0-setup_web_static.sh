#!/usr/bin/env bash
apt-get update
apt-get install -y nginx

sudo mkdir -p /data/web_static/releases/test/
sudo mkdir -p /data/web_static/shared

echo "<html>
  <head>
  </head>
  <body>
    Hello World!
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html

sudo ln -sf /data/web_static/releases/test/ /data/web_static/current

# Give ownership of /dada/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

sed -i '/server {/a \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}' /etc/nginx/sites-available/default

service nginx restart
