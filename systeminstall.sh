#!/bin/bash
# Instala o tfiles como comando do sistema.
apt-get install python3
cp "tfiles.py" "/usr/bin/tfiles"
chmod +x "/usr/bin/tfiles"
apt-get update
apt-get install python3-pip
apt-get install xclip
python3 -m pip install clipboard
python3 -m pip install keyboard
