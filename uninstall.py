import os
try:
    os.remove("/usr/bin/tfiles")
except PermissionError:
    print("É preciso executar como root.")
