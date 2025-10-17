echo "Checking root permissions..."

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root."
    exit 1
fi

echo "Removing files"
rm -rf /opt/tfiles

echo "Removing binaries"
rm /usr/bin/tfiles