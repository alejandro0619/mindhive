#!/bin/bash

if [[ "$(uname -s)" == MINGW* ]]; then
    # Windows specific commands
    PYTHONPATH=$PYTHONPATH:$(dirname $(which pylint)) # add pylint installation directory to PYTHONPATH on Windows
    git_cmd='git.cmd'
else
    # Linux specific commands
    git_cmd='git'
    if command -v pylint &> /dev/null
    then
      echo "Pylint is already installed"
    else
      echo "Pylint is not installed. Installing now..."
      pip install pylint
    fi
fi

# run pylint on all python files in the git repository
$git_cmd ls-files '*.py' | xargs pylint > report_linter.txt

