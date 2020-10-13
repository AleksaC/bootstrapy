#!/usr/bin/env python

import os
import re
import sys

from typing import Dict
from typing import Set
from typing import Union


VARIABLE_RE = re.compile("___(?P<var_name>[a-zA-Z_][a-zA-Z_0-9]*)___")

PROJECT_REMOTE = "git@github.com:AleksaC/test-template.git"

IGNORE = {
    ".git",
    ".idea",
    ".vscode",
    "venv",
    "_build",
    "dist",
    "build",
    "__pycache__",
    "library.egg-info",
}

variables = {"repo_name"}
file_paths: Set[str] = set()
file_contents = {}


def traverse_repo(root: Union[str, os.DirEntry]) -> None:
    with os.scandir(root) as it:
        for entry in it:
            name = entry.name
            if name not in IGNORE:
                variable = re.match(VARIABLE_RE, name)
                if variable:
                    var_name = variable.group("var_name")
                    variables.add(var_name)
                    path = entry.path
                    for fp in file_paths.copy():
                        if path.startswith(fp):
                            file_paths.remove(fp)
                            break
                    file_paths.add(path)
                if entry.is_dir():
                    traverse_repo(entry)
                else:
                    with open(entry.path) as f:
                        try:
                            contents = f.read()
                            var = set(re.findall(VARIABLE_RE, contents))
                            if var:
                                variables.update(var)
                                file_contents[entry.path] = var
                        except UnicodeDecodeError:
                            pass


def inquire(variables: Set[str]) -> Dict[str, str]:
    values = {}
    print("Enter the values for the following variables:")
    for variable in variables:
        values[variable] = input(f"{variable}: ")
    return values


def render_files(fc: Dict[str, Set[str]], values: Dict[str, str]) -> None:
    for fp, vrs in fc.items():
        with open(fp, "r+") as f:
            c = f.read()
            for var in vrs:
                c = c.replace(f"___{var}___", values[var])
            f.seek(0)
            f.write(c)
            f.truncate()


def render_paths(fps: Set[str], values: Dict[str, str]) -> None:
    for fp in fps:
        path = ""
        for name in re.split(VARIABLE_RE, fp):
            if name in values:
                extended_path = path + values[name]
                os.rename(f"{path}___{name}___", extended_path)
                path = extended_path
            else:
                path += name


def bootstrap() -> None:
    if __file__ == "<stdin>":
        os.system("git clone %s ___repo_name___" % PROJECT_REMOTE)
        os.execl(sys.executable, sys.executable, "___repo_name___/bootstrap.py")

    if not sys.stdin.isatty():
        sys.stdin = open("/dev/tty")

    traverse_repo("___repo_name___")
    values = inquire(variables)
    render_files(file_contents, values)
    render_paths(file_paths, values)

    os.remove(os.path.realpath(__file__))


def main() -> int:
    bootstrap()
    return 0


if __name__ == "__main__":
    sys.exit(main())
