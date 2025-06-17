#!/bin/bash

mkdir -p /opt/tfiles
cp ./* -R /opt/tfiles

chmod +x /opt/tfiles/tfiles.py

if command -v apt-get >/dev/null 2>&1; then
    apt-get install python3-venv
elif command -v yum >/dev/null 2>&1; then
    yum install python3-venv
elif command -v dnf >/dev/null 2>&1; then
    dnf install python3-venv
else
    echo "Install python3-venv manually if not installed."
fi

python3 -m venv /opt/tfiles/venv
/opt/tfiles/venv/bin/python3 -m pip install -r requirements.txt

touch /usr/bin/tfiles
echo "#!/bin/bash" >> /usr/bin/tfiles
echo "/opt/tfiles/venv/bin/python3 /opt/tfiles/tfiles.py" >> /usr/bin/tfiles

chmod +x /usr/bin/tfiles
