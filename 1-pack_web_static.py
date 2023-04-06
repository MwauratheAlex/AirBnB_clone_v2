#!/usr/bin/python3
"""A Fabric script that generates a .tgz archive from the contents
of the web_static folder of your AirBnB Clone repo."""

import tarfile
import os
from datetime import datetime
from fabric.api import local


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
