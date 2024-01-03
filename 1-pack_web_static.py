#!/usr/bin/python3
from fabric.api import local
from datetime import datetime


def do_pack():
    """ 
    A function that generates archive from the contents of web_static folder
    """

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    try:
        # Create the versions' folder if it doesn't exist
        local("mkdir -p versions")

        # Set the archive name
        archive_name = "web_static_{}.tgz".format(timestamp)

        # Compress the contents of the web_static folder
        local("tar -cvzf versions/{} web_static".format(archive_name))

        return "versions/{}".format(archive_name)

    except Exception as e:
        return None
