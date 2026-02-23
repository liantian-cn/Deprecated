# coding:utf-8
import base64

from PySide6.QtCore import Qt, QByteArray
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QSystemTrayIcon
from qfluentwidgets import (FluentWindow, FluentIcon, SubtitleLabel, setFont, NavigationItemPosition, SystemTrayMenu,
                            Action)

from app.resource.logo2 import image_data as image_data_base64
from .generate_interface import GenerateInterface
from .macro_interface import MacroInterface
from .property_interface import PropertyInterface
from .public_func_interface import PublicFuncInterface
from .rotation_interface import RotationInterface
from .running_interface import RunningInterface
from .setting_interface import SettingInterface
from .snippet_interface import SnippetInterface
from app.common.utils import generate_unique_strings


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class Window(FluentWindow):

    def __init__(self):
        super().__init__()

        # create sub interface
        self.settingInterface = SettingInterface(self)
        self.propertyInterface = None
        self.rotationInterface = None
        self.macroInterface = None
        self.botInterface = None
        self.generateInterface = None
        self.runningInterface = None
        self.snippetInterface = None
        self.publicFuncInterface = None

        self.activation = False
        self.current_profile = None

        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, '设置')

        image_data = base64.b64decode(image_data_base64)
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(image_data))
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

        self.resize(1440, 900)
        # self.showMaximized()
        # self.setFixedSize(self.width(), self.height())
        t = generate_unique_strings(4, 4)

        self.setWindowTitle("-".join(t))

        self.titleBar.maxBtn.hide()
        self.titleBar.minBtn.hide()

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        # self.setFixedSize(w, h-24)

        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

        self.tray_icon = QSystemTrayIcon(icon, self)
        self.tray_icon.setVisible(True)
        self.tray_menu = SystemTrayMenu()

        restore_action = Action("恢复", self)
        restore_action.triggered.connect(self.show)
        self.tray_menu.addAction(restore_action)

        exit_action = Action("退出", self)
        exit_action.triggered.connect(self.exit_application)
        self.tray_menu.addAction(exit_action)

        self.tray_icon.setContextMenu(self.tray_menu)
        self.tray_icon.activated.connect(self.on_tray_icon_activated)

        self.stackedWidget.currentChanged.connect(self.onActivated)

        self.profile_name = None
        self.profile = {}
        self.username = None

    def onActivated(self, index):
        current_widget = self.stackedWidget.currentWidget()
        if hasattr(current_widget, 'onActivated') and callable(getattr(current_widget, 'onActivated')):
            current_widget.onActivated()  # 调用 onActivated 方法
        else:
            print("onActivated method not defined or not callable.")

    def activate_software(self):
        if not self.activation:
            self.propertyInterface = PropertyInterface(self)
            self.rotationInterface = RotationInterface(self)
            self.macroInterface = MacroInterface(self)
            self.generateInterface = GenerateInterface(self)
            self.runningInterface = RunningInterface(self)
            self.snippetInterface = SnippetInterface(self)
            self.publicFuncInterface = PublicFuncInterface(self)

            self.navigationInterface.addSeparator()
            self.addSubInterface(self.rotationInterface, FluentIcon.DEVELOPER_TOOLS, '战斗逻辑设置')
            self.addSubInterface(self.propertyInterface, FluentIcon.DEVELOPER_TOOLS, '属性设置')
            self.addSubInterface(self.macroInterface, FluentIcon.DEVELOPER_TOOLS, '宏设置')
            self.addSubInterface(self.publicFuncInterface, FluentIcon.DEVELOPER_TOOLS, '怪物技能设置')
            self.navigationInterface.addSeparator()
            self.addSubInterface(self.generateInterface, FluentIcon.PRINT, '生成器')
            self.addSubInterface(self.runningInterface, FluentIcon.PLAY, '执行')

            self.addSubInterface(self.snippetInterface, FluentIcon.QUICK_NOTE, '在线代码块',
                                 NavigationItemPosition.BOTTOM)

            self.settingInterface.activate_software()
            self.activation = True

    def closeEvent(self, event):
        event.ignore()  # 忽略关闭事件
        self.hide()  # 隐藏窗口

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.DoubleClick:
            self.show()  # 双击托盘图标时显示窗口
            self.activateWindow()  # 激活窗口

    def exit_application(self):
        self.tray_icon.hide()  # 隐藏托盘图标
        QApplication.quit()  # 退出应用
