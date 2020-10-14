#!/usr/bin/env python

import os
import re
import shutil
import sys
from urllib.error import HTTPError
from urllib.request import Request
from urllib.request import urlopen

from typing import Dict
from typing import Set
from typing import Union


VARIABLE_RE = re.compile("___(?P<var_name>[a-zA-Z_][a-zA-Z_0-9]*)___")

PROJECT_REMOTE = "git@github.com:AleksaC/test-template.git"

# TODO: Look for a better way of excluding files than hard-coding them here.
#  Maybe try parsing .gitignore (.git should stay hardcoded anyway)
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

variables: Set[str] = set()
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


def create_github_repo(repo_name: str) -> str:
    user_or_org = ""
    while user_or_org not in {"u", "o"}:
        user_or_org = input(
            "Are you creating a repository for a user or an organization? [u/o] "
        )
    print()
    user = user_or_org == "u"
    user_or_org_name = input(f"{'User' if user else 'Organization'} name: ")
    token = input("Enter github personal access token: ")

    url = "https://api.github.com/"
    if user:
        url += "user/repos"
    else:
        url += f"orgs/{user_or_org_name}/repos"
    headers = {"Authorization": f"token {token}"}
    data = f'{{"name":"{repo_name}"}}'

    req = Request(url, headers=headers, data=data.encode())
    print("\nCreating GitHub repo...\n")
    try:
        resp = urlopen(req)
    except HTTPError as e:
        print(
            "Something went wrong - please check that the repository with the name "
            f"{repo_name} doesn't already exist. Also make sure that the personal "
            "access token you provided is correct."
        )
        print(e)
        return ""

    if resp.getcode() == 201:
        return f"{user_or_org_name}/{repo_name}"

    return ""


def push_to_github(repo_path: str) -> int:
    url = f"git@github.com:{repo_path}"

    commands = [
        "git add .",
        "git commit -m 'Initial commit'",
        f"git remote add origin {url}",
        "git push -u origin HEAD",
    ]

    for command in commands:
        status = os.system(command)
        if status != 0:
            return status

    return 0


def main() -> int:
    if __file__ == "<stdin>":
        os.system(f"git clone --depth 1 {PROJECT_REMOTE} ___repo_name___")
        os.execl(
            sys.executable,
            sys.executable,
            os.path.join("___repo_name___", "bootstrap.py"),
        )

    if not sys.stdin.isatty():
        sys.stdin = open("/dev/tty")

    repo_path = os.path.dirname(os.path.realpath(__file__))
    os.chdir(repo_path)

    if os.path.exists(".git"):
        shutil.rmtree(".git")

    traverse_repo(os.getcwd())
    values = inquire(variables)
    render_files(file_contents, values)
    render_paths(file_paths, values)

    print()
    os.system("git init")
    print()

    os.remove(os.path.join(os.getcwd(), os.path.basename(__file__)))

    publish_to_github = ""
    while publish_to_github not in {"y", "n"}:
        publish_to_github = input(
            "Publish the repo to github? (Requires personal access token) [y/n] "
        )

    if publish_to_github == "y":
        print()
        repo_path = create_github_repo(values["repo_name"])
        if repo_path:
            push_to_github(repo_path)
        else:
            print("Could not create the repository!")

    return 0


if __name__ == "__main__":
    sys.exit(main())
