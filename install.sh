#!/bin/bash
apt-get install python3
touch "/usr/bin/tfiles"
echo "" > "/usr/bin/tfiles"
echo "#!/bin/bash" >> "/usr/bin/tfiles"
echo "python3 '/opt/tfiles/script/tfiles.py'" >> "/usr/bin/tfiles"
chmod +x "/usr/bin/tfiles"
mkdir "/opt/tfiles"
mkdir "/opt/tfiles/script"
cp "tfiles.py" "/opt/tfiles/script/tfiles.py"
cp "uninstall.py" "/opt/tfiles/uninstall.py"
cp "uninstall.sh" "/opt/tfiles/uninstall.sh"
apt-get update
apt-get install python3-pip
apt-get install xclip
python3 -m pip install clipboard
groupadd "tfiles"
python3 "config.py"
usermod -a -G tfiles "root"
chgrp "tfiles" "/opt/tfiles" -R
chmod g+rwx  "/opt/tfiles" -R
