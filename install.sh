#!/bin/bash
cd "$(dirname "$0")"

echo "Copying files to instalaition directory..."
mkdir -p /opt/tfiles
cp ./* -R /opt/tfiles

echo "Installing python3-venv..."
if command -v apt-get >/dev/null 2>&1; then
    apt-get install python3-venv
elif command -v yum >/dev/null 2>&1; then
    yum install python3-venv
elif command -v dnf >/dev/null 2>&1; then
    dnf install python3-venv
else
    echo "Install python3-venv manually if not installed."
fi

echo "Installing requirements..."
python3 -m venv /opt/tfiles/venv
/opt/tfiles/venv/bin/python3 -m pip install -r requirements.txt

echo "Creating tfiles command..."
cp run.sh /usr/bin/tfiles

echo "Setting permissions..."
chmod +x /opt/tfiles/tfiles.py
chmod +x /usr/bin/tfiles

echo "Done."
