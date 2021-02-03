import os
print("Obrigado por usar o tfiles!")

try:
    os.remove("/usr/bin/tfiles")
except PermissionError:
    print('\033[31mOps! Você precisa rodar o desinstalador como root!')
    exit()
os.system("rm -r '/opt/tfiles/script' ")
for files in os.listdir("/opt/tfiles/"):
    os.remove(f'/opt/tfiles/{files}')
