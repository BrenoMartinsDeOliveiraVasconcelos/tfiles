#!/bin/bash
set -e

APP_NAME="tfiles"
INSTALL_DIR="/opt/${APP_NAME}"
CONFIG_FILE="${INSTALL_DIR}/config.json"
CONFIG_BAK="${CONFIG_FILE}.bak"
BIN_PATH="/usr/bin/${APP_NAME}"
VENV_DIR="${INSTALL_DIR}/venv"
VENV_PKG="python3-venv"


cd "$(dirname "$0")"

echo "Checking root permissions..."
if [ "$EUID" -ne 0 ]; then
    echo "Please run as root."
    exit 1
fi

echo "Checking if config file exists already..."
if [ -f "$CONFIG_FILE" ]; then
    echo "Saving config file..."

    if [ ! -e "$CONFIG_BAK" ]; then
        mv "$CONFIG_FILE" "$CONFIG_BAK"
    else
        echo "Found a bak file that is not removed. Maybe the script was ran for a second time by accident? Not overwriting."
    fi
fi

echo "Copying files to installation directory..."
mkdir -p "$INSTALL_DIR"

files=("config.json" "helpers.py" "init.py" "tfiles.py" "translations" "uninstall.sh" "requirements.txt" "README.md" "LICENSE.md" "run.sh")

for file in "${files[@]}"; do
    cp "./$file" -R "$INSTALL_DIR"
done

echo "Installing ${VENV_PKG}..."
if command -v apt-get >/dev/null 2>&1; then
    apt-get install "${VENV_PKG}" -y
elif command -v yum >/dev/null 2>&1; then
    yum install "${VENV_PKG}" -y
elif command -v dnf >/dev/null 2>&1; then
    dnf install "${VENV_PKG}" -y
else
    echo "Install ${VENV_PKG} manually if not installed."
fi

echo "Checking installation..."
python3 -c "import venv"
if [ $? -ne 0 ]; then
    echo "Python 'venv' module is not installed. Please install it and re-run the script."
    exit 1
fi

echo "Installing requirements..."
python3 -m venv "$VENV_DIR"

cd "$INSTALL_DIR"

"${VENV_DIR}/bin/python3" -m pip install -r requirements.txt

echo "Creating ${APP_NAME} command..."
rm -rf "$BIN_PATH"
ln -s "${INSTALL_DIR}/run.sh" "$BIN_PATH"

echo "Setting permissions..."

chmod +x "$BIN_PATH"

chmod 777 "$INSTALL_DIR"

find "$INSTALL_DIR" -type d -exec chmod 755 {} \;
find "$INSTALL_DIR" -type f -exec chmod 755 {} \;
find "$INSTALL_DIR" -name "*.json*" -exec chmod 777 {} \;

echo "Done."