import os
from pathlib import Path
from shutil import copy, copytree
from distutils.sysconfig import get_python_lib
from datetime import datetime

x = int((datetime.now() - datetime(2023, 7, 1)).days)
now = datetime.now()

args = [
    'nuitka',
    # '--standalone',
    '--onefile',
    '--assume-yes-for-downloads',
    '--windows-uac-admin',
    '--mingw64',
    '--windows-icon-from-ico=E:/Documents/GitHub/PixelRotationLT/resource/images/favicon.ico',
    '--enable-plugins=pyside6',
    '--windows-console-mode=disable',
    '--show-progress',
    '--output-dir=build',
    '--product-name="Microsoft Edge"',
    f'--product-version=133.0.3076.92',
    f'--file-version=133.0.3076.92',
    f'--file-description="Microsoft Edge"',
    f'--copyright="Copyright (C) {now.strftime("%Y-%m-%d %H:%M:%S")} github.com/liantian-cn"',
    'msedge.py',
]

os.system(' '.join(args))

# copy site-packages to dist folder
# dist_folder = Path("dist/main/main.dist")
# site_packages = Path(get_python_lib())
#
# copied_libs = []
#
# for src in copied_libs:
#     src = site_packages / src
#     dist = dist_folder / src.name
#
#     print(f"Coping site-packages `{src}` to `{dist}`")
#
#     try:
#         if src.is_file():
#             copy(src, dist)
#         else:
#             copytree(src, dist)
#     except:
#         pass
#
#
# # copy standard library
# copied_files = ["ctypes", "hashlib.py", "hmac.py", "random.py", "secrets.py", "uuid.py"]
# for file in copied_files:
#     src = site_packages.parent / file
#     dist = dist_folder / src.name
#
#     print(f"Coping stand library `{src}` to `{dist}`")
#
#     try:
#         if src.is_file():
#             copy(src, dist)
#         else:
#             copytree(src, dist)
#     except:
#         pass
