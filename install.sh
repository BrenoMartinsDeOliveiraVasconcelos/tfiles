#!/bin/bash
# Instala os componentes necessários para rodar o tfiles.
apt-get install python3
apt-get update
apt-get install python3-pip
apt-get install xclip
python3 -m pip install clipboard
python3 -m pip install keyboard
