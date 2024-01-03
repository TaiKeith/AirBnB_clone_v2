#!/usr/bin/python3
"""
This script creates and distributes an archive from the
web_static folder to my web servers using the function deploy
"""

from fabric.api import *
from datetime import datetime
import os


env.hosts = ['54.227.221.46', '52.86.160.210']
env.user = "ubuntu"
env.key_filename = '~/.ssh/id_rsa'


def do_pack():
    """
    A function that generates archive from the contents of web_static folder
    """
    try:
        local("mkdir -p versions")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        archive_path = "versions/web_static_{}.tgz".format(timestamp)
        local("tar -czvf {} web_static".format(archive_path))
        return archive_path
    except Exception as e:
        print(e)
        return None


def do_deploy(archive_path):
    """
    This function distributes an archive to my web servers
    """
    if not os.path.exists(archive_path):
        return False

    try:
        # Upload the archive to /tmp/ directory of the web server
        put(archive_path, '/tmp/')

        # Extract the archive to /data/web_static/releases/<archive filename>
        archive_filename = os.path.basename(archive_path)
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


def deploy():
    """
    Deploy the web_static content to web servers
    """
    archive_path = do_pack()

    if not archive_path:
        return False

    return do_deploy(archive_path)
