#!/usr/bin/env python

from __future__ import print_function

import os
import sys

if __name__ == "__main__":
    if __file__ == "<stdin>":
        os.system("git clone git@github.com:AleksaC/drf-base.git __project__")
        os.execl(sys.executable, sys.executable, "__project__/bootstrap.py")

    if not sys.stdin.isatty():
        sys.stdin = open("/dev/tty")

    project_name = input("Project_name: ")

    path = os.path.realpath(__file__)
    project_base = os.path.dirname(path)
    project_base_location = os.path.dirname(project_base)
    new_project_base = os.path.join(project_base_location, project_name)

    os.rename(project_base, new_project_base)

    current_file_name = os.path.basename(path)
    os.remove(os.path.join(new_project_base, current_file_name))
