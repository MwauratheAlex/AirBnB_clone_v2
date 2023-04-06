#!/usr/bin/python3
"""A Fabric script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone repo."""

import tarfile
import os
from datetime import datetime
from fabric.api import *


env.hosts = ["34.229.161.179", "52.201.180.153"]


def do_pack():
    """generates a .tgz archive from the contents of the web_static folder
    of AirBnB Clone repo"""
    output_dir = "versions"
    try:
        os.mkdir(output_dir)
    except OSError:
        pass

    now = datetime.now().strftime("%Y%m%d%H%M%S")
    output_filename = "web_static_" + now + ".tgz"
    archive_path = "./{}/{}".format(output_dir, output_filename)

    local("tar -cvzf {} web_static".format(archive_path))

    if os.path.exists(archive_path):
        return archive_path
    else:
        return None


def do_deploy(archive_path):
    """distributes an archive to your web servers"""
    if os.path.exists(archive_path) is False:
        return False

    filename = archive_path[archive_path.index("web_static"):]
    output_filename = filename[: -4]

    if put(archive_path, "/tmp/{}".format(filename)).failed:
        return False
    if run("mkdir -p /data/web_static/releases/{}/"
           .format(output_filename)).failed:
        return False
    if run("tar -xzf /tmp/{} -C /data/web_static/releases/{}"
           .format(filename, output_filename)).failed:
        return False
    if run("rm /tmp/{}".format(filename)).failed:
        return False
    if run("mv /data/web_static/releases/{}/web_static/* "
           "/data/web_static/releases/{}/ "
           .format(output_filename, output_filename)).failed:
        return False
    if run("rm -rf /data/web_static/releases/{}/web_static"
           .format(output_filename)).failed:
        return False
    if run("rm -rf /data/web_static/current").failed:
        return False
    if run("ln -s /data/web_static/releases/{}/ /data/web_static/current"
           .format(output_filename)).failed:
        return False


def deploy():
    """creates and distributes an archive to your web servers"""
    archive_path = do_pack()

    if archive_path is None:
        return False
    else:
        return do_deploy(archive_path)
