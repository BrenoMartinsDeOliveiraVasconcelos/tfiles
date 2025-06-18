#!/bin/bash
cd "$(dirname "$0")"


echo "Checking root permissions..."
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root."
    exit 1
fi


echo "Checking if config file exists already..."
if [ -f "/opt/tfiles/config.json" ]; then
    echo "Saving config file..."
    mv /opt/tfiles/config.json /opt/tfiles/config.json.bak
fi

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


echo "Checking installation..."
python3 -c "import venv"
if [ $? -ne 0 ]; then
    echo "Python 'venv' module is not installed. Please install it and re-run the script."
    exit 1
fi

echo "Installing requirements..."
python3 -m venv /opt/tfiles/venv
/opt/tfiles/venv/bin/python3 -m pip install -r requirements.txt

echo "Creating tfiles command..."
cp run.sh /usr/bin/tfiles

echo "Setting permissions..."
chmod +x /usr/bin/tfiles
find /opt/tfiles -type d -exec chmod 777 {} \;
find /opt/tfiles -type f -exec chmod 777 {} \;

echo "Done."
