import os
from pathlib import Path
from shutil import copy, copytree
from distutils.sysconfig import get_python_lib
from datetime import datetime

x = int((datetime.now() - datetime(2023, 7, 1)).days)
now = datetime.now()

BASE_DIR = Path(__file__).parent

app_content = open("ShionAppDev.py", "r", encoding="utf-8").read()
app_content = app_content.replace("DEV_MODE = True", "DEV_MODE = False")
with open("ShionApp.py", "w", encoding="utf-8") as f:
    f.write(app_content)

args = [
    'nuitka',
    '--standalone',
    # '--onefile',
    '--assume-yes-for-downloads',
    # '--windows-uac-admin',
    '--mingw64',
    '--windows-icon-from-ico=E:/Documents/GitHub/Shion/favicon.ico',
    '--enable-plugins=pyside6',
    '--windows-console-mode=attach',
    '--show-progress',
    '--output-dir=build',
    '--product-name="ShionApp"',
    '--product-version=0.0.1',
    'ShionApp.py',
]

os.system(' '.join(args))

args = [
    'nuitka',
    '--standalone',
    # '--onefile',
    '--assume-yes-for-downloads',
    # '--windows-uac-admin',
    '--mingw64',
    '--windows-icon-from-ico=E:/Documents/GitHub/Shion/favicon.ico',
    '--enable-plugins=pyside6',
    '--windows-console-mode=attach',
    '--show-progress',
    '--output-dir=build',
    '--product-name="ShionApp SN Generator"',
    '--product-version=0.0.1',
    'genSN.py',
]

os.system(' '.join(args))

# copy standard library
for file in list(BASE_DIR.glob("*.rkf"))+list(BASE_DIR.glob("*.lkf"))+list(BASE_DIR.glob("*.key")):
    src = file
    dist = BASE_DIR.joinpath("build") / src.name
    print(f"Coping `{src}` to `{dist}`")
    copy(src, dist)

