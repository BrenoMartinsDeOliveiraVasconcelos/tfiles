#!/bin/bash
apt-get install python3
touch "/usr/bin/tfiles"
echo "" > "/usr/bin/tfiles"
echo "#!/bin/bash" >> "/usr/bin/tfiles"
echo "python3 '/opt/tfiles/script/tfiles.py'" >> "/usr/bin/tfiles"
chmod +x "/usr/bin/tfiles"
mkdir "/opt/tfiles"
mkdir "/opt/tfiles/script"
touch "/opt/tfiles/cdt"
echo "33" > "/opt/tfiles/cdt"
touch "/opt/tfiles/deco"
echo "⚘ = * •" > "/opt/tfiles/deco"
cp "tfiles.py" "/opt/tfiles/script/tfiles.py"
cp "unistall.py" "/opt/tfiles/unistall.py"
apt-get install python3-pip
apt-get install xclip
python3 -m pip install clipboard
groupadd "tfiles"
python3 "config.py"
usermod -a -G tfiles "root"
chgrp "tfiles" "/opt/tfiles" -R
chmod g+rwx  "/opt/tfiles" -R
