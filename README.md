# bootstrapy

[![license](https://img.shields.io/badge/License-MIT-green.svg)](https://github.com/AleksaC/bootstrapy/blob/master/LICENSE)
[![Build Status](https://dev.azure.com/aleksac/bootstrapy/_apis/build/status/AleksaC.bootstrapy?repoName=AleksaC%2Fbootstrapy&branchName=master)](https://dev.azure.com/aleksac/bootstrapy/_build?definitionId=5&branchName=master)
[![Coverage](https://img.shields.io/azure-devops/coverage/aleksac/bootstrapy/5/master.svg)](https://dev.azure.com/aleksac/bootstrapy/_build/latest?definitionId=5&branchName=master)
<a href="https://github.com/psf/black"><img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg"></a>
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/AleksaC/bootstrapy/blob/master/.pre-commit-config.yaml)

Generate projects from templates with a single command.

## About 📖
While working on a bunch of projects I noticed that many of them share some structure.
In some cases I extract that common functionality in a template which I then use
as starting point for developing my future projects. After starting a project from
a template I need to rename the appropriate files and search and replace some names
and values inside the the template. The former part is tedious and the later part
is error-prone. For this reason I decided to try to automate this by creating `bootstrapy`.

`bootstrapy` walks the template directory looking for patterns that start and end
with triple underscore both in file and directory names and file contents. These
patterns represent variables, and once all of them have been found the user is
prompted to enter the value of each variable. When the user enters the values of
all the variables the values are used to replace the variables. The reason I chose
underscores as delimiters is because they are valid variable names in all relevant
programming languages, and I used 3 of them because I thought that this is very
unlikely to collide with names of variables or special constructs in languages
like python's dunder methods.

Beside the search and replace functionality `bootstrapy` offers a few other
functionalities such as automatically creating the repo for the new project using
[GitHub PAT](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token)
and pushing the newly rendered project to it.

Note that `bootstrapy` isn't a framework or a CLI tool it is just a file that you
put inside your template to make it easier to bootstrap the project from it. It
doesn't use any third-party dependencies, and the only prerequisite for using it
is having `python >=3.6` installed.

To better understand the how this tool works take a look at
[one of my templates that uses it](https://github.com/AleksaC/python-library-base).

### Why not cookiecutter
Those that are familiar with project templating might be wondering why I wrote this
instead of simply using [cookiecutter](https://github.com/cookiecutter/cookiecutter).
The main problem I had with cookiecutter when I tried it is the usage of `jinja2`
templates which breaks syntax of many languages and sometimes even causes problems
in the names of the files. For example this is not valid python syntax:
```python
from {{cookiecutter.foo}} import bar
```
This means that I cannot develop my templates as they are but have to change variable
names back and forth as I switch between development and releases.

Another 'flaw' of cookiecutter is that you have to install
it in order to use the template. I wanted to make using my templates as easy as
executing a single command with no prior installations.

**Note**: I'm not saying that cookiecutter is bad, or that it's usage of `jinja2`
templates is an unreasonable choice. On the contrary, it absolutely make sense
to use a full-fledged templating engine for complex templates. However since I
don't use any advanced features I get virtually no benefits and all the downsides.

## Getting started ⚙️
To use bootstrapy simply copy the `bootstrap.py` file from this repo and put it in
your template repo and replace the value of `PROJECT_REMOTE` variable at the top
of the script with the url to your repository.

After you follow the instructions above you will be able to generate projects from
your template like in the following example that uses a
[template for python library](https://github.com/AleksaC/python-library-base):
```shell script
wget -O - "https://raw.githubusercontent.com/AleksaC/python-library-base/master/bootstrap.py" | python
```

## Contact 🙋‍♂️
- [Personal website](https://aleksac.me)
- <a target="_blank" href="http://twitter.com/aleksa_c_"><img alt='Twitter followers' src="https://img.shields.io/twitter/follow/aleksa_c_.svg?style=social"></a>
- aleksacukovic1@gmail.com
