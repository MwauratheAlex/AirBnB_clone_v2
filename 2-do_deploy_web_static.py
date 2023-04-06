#!/usr/bin/python3
"""distributes an archive to web servers"""
from fabric.api import *
import os

env.hosts = ["34.229.161.179", "52.201.180.153"]


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
