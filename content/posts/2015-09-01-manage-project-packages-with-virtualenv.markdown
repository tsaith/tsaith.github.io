Title: Manage project packages with virtualenv
Date: 2015-09-01
Tags: python
Category: Misc


While developing two or more projects at the same time,
it is unavoidable to switch among projects which may use the same python package of different version.
In order to resolve the headache of package management,
[virtualenv](https://virtualenv.pypa.io/en/latest/) is designed to create isolated python environments.

### Install virtualenv

Open your terminal and execute
```
pip3 install virtualenv virtualenvwrapper
```
where [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/) is a set of extension of `virtualenv`.

### Set environment variables

In `~/.profile`, add the lines below :
```
export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python3
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```
Followed by reloading `~/.profile` :
```
source ~/.profile
```

### Some examples of usage

To create a new project environment named `vision` with python 3.4 support :
```
$ mkvirtualenv -p /usr/local/bin/python3.4 vision

```

In case we want to install [ipython](http://ipython.org/) under `vision` environment :
```
pip install ipython[notebook]
```

To leave the environment of current project :
```
deactivate
```

To work on a existed project :
```
workon project_name
```
