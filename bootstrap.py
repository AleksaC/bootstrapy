#!/usr/bin/env python
import os
import sys

PROJECT_REMOTE = "git@github.com:AleksaC/drf-base.git __project__"


def bootstrap():
    if __file__ == "<stdin>":
        os.system("git clone %s" % PROJECT_REMOTE)
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


def main():
    return 0


if __name__ == "__main__":
    sys.exit(main())
