# coding:utf-8
import sys
import ctypes
from PySide6.QtWidgets import QApplication
from qfluentwidgets import (setTheme, Theme)

from app.view.main_window import Window


if __name__ == '__main__':

    mutex_name = "Global\\PixelRotationMutex"

    # 创建或打开互斥锁
    mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)

    # 检查互斥锁的返回值
    if ctypes.windll.kernel32.GetLastError() == 183:
        print("脚本已经在运行。")
        sys.exit()

    from app.common.utils import init_utils
    init_utils()
    from app.common.config import init_config
    init_config()
    setTheme(Theme.AUTO)

    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
