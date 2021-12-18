#!/bin/bash

# It's very platform specific script

SEALGULL_ENV_NAME="sealgull-venv"

if [ ! -d ~/venvs/ ];
then
    echo "Folder for venvs doesn't exist! Let's create it"
    mkdir ~/venvs
fi

cd ~/venvs

if [ ! -d ~/venvs/$SEALGULL_ENV_NAME ];
then
    echo "Production enviroment doesn't exist! Let's create it"
    python3 -m venv $SEALGULL_ENV_NAME
fi

source ~/venvs/$SEALGULL_ENV_NAME/bin/activate

cd ~/SealGull/
pip3 install -r requirements.txt

cd ~/SealGull/script
