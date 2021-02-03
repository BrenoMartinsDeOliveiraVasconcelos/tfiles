import os

users = os.listdir("/home/")
for user in users:
    os.system(f"sudo usermod -a -G tfiles {user}")
