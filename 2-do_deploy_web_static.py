#!/usr/bin/python3
"""
This script distributes an archive to my web servers using the function
do_deploy
"""

from fabric.api import *
from datetime import datetime
import os


env.hosts = ['100.26.253.187', '54.210.161.190']
env.user = "ubuntu"
env.key_filename = '~/.ssh/school'


def do_pack():
    """
    A function that generates archive from the contents of web_static folder
    """

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    try:
        # Create the versions' folder if it doesn't exist
        local("mkdir -p versions")

        # Set the archive name
        archive_path = "web_static_{}.tgz".format(timestamp)

        # Compress the contents of the web_static folder
        local("tar -cvzf versions/{} web_static".format(archive_path))

        return "versions/{}".format(archive_path)

    except Exception as e:
        return None


def do_deploy(archive_path):
    """
    This function distributes an archive to my web servers.
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Extract the archive filename
        archive = archive_path.split('/')[-1]
        archive_filename = "/tmp/{}".format(archive)
        folder_name = archive.split('.')[0]
        release_path = "/data/web_static/releases/{}/".format(folder_name)

        # Upload the archive to the /tmp/ directory on the web server
        put(archive_path, archive_filename)

        # Create the release directory
        run('mkdir -p {}'.format(release_path))

        # Extract the archive to the release directory
        run('tar -xzf {} -C {}'.format(archive_filename, release_path))

        # Remove the archive from the web server
        run('rm {}'.format(archive_filename))

        # Move the contents out of the web_static folder
        run('mv {}/web_static/* {}'.format(release_path, release_path))
        run('rm -rf {}/web_static'.format(release_path))

        # Remove the existing symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s {} /data/web_static/current'.format(release_path))

        print("New version deployed!")
        return True

    except Exception as e:
        print(f"Deployment failed: {e}")
        return False
