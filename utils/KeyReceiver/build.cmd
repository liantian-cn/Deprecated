python -m nuitka --recurse-all --recurse-directory=pyautogui --windows-icon=icon.ico  --output-dir=dist server.py
python -m nuitka --recurse-all --recurse-directory=keyboard  --windows-icon=icon.ico --output-dir=dist client.py
python -m nuitka --recurse-all --recurse-directory=keyboard  --windows-icon=icon.ico --output-dir=dist get_code.py