#!/usr/bin/python3
"""
This script distributes an archive to my web servers using the function
do_deploy
"""

from fabric.api import *
from datetime import datetime
import os


env.hosts = ['54.227.221.46', '52.86.160.210']
env.user = "ubuntu"
env.key_filename = '~/.ssh/id_rsa'


def do_deploy(archive_name):
    """
    This function distributes an archive to my web servers
    """
    if not os.path.exists(archive_name):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web server
        put(archive_name, '/tmp/')

        # Extract the archive to /data/web_static/releases/<archive filename>
        archive_filename = os.path.basename(archive_name)
        folder_name = os.path.splitext(archive_filename)[0]
        release_path = os.path.join('/data/web_static/releases', folder_name)

        run('mkdir -p {}'.format(release_path))
        run('tar -xzf /tmp/{} -C {}'.format(archive_filename, release_path))

        # Delete the archive from the web server
        run('rm /tmp/{}'.format(archive_filename))

        run('mv {}/web_static/* {}'.format(release_path, release_path))
        run('rm -rf {}/web_static'.format(release_path))

        # Delete the symbolic link
        run('rm -rf /data/web_static/current')

        # Create a new symbolic link
        run('ln -s {} /data/web_static/current'.format(release_path))

        print("New version deployed!")
        return True

    except Exception as e:
        print(e)
        return False
