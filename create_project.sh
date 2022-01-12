#! /bin/bash

# In your .zshrc or bash profile you have to add a Export line
# Do
# nano .zshrc
# or when using Bash
# nano ~/.bash_profile
# add this line at the end of the file with the correct path to this script
# export PATH=~/MyBashScripts/all_scripts:$PATH

# in this script put the correct folder name here something like this after DIR=
DIR=~/MyPythonProjects/initialize_project_with_python

# Leave this part be!
source $DIR/.venv/bin/activate
# virtualenv is now active.
python $DIR/create_project.py