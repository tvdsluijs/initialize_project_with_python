#! /bin/bash
DIR=$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )

source $DIR/venv/bin/activate

# virtualenv is now active.

python $DIR/create_project.py