# coding:utf-8
import random
import time
from datetime import datetime

import d3dshot
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtGui import QColor, QPainter, QTextCursor, QPen
from PySide6.QtWidgets import (QHBoxLayout, QWidget, QVBoxLayout, QSizePolicy, QHeaderView, QTableWidgetItem)
from qfluentwidgets import (BodyLabel, PrimaryPushButton, ScrollArea, FluentIcon, PushButton, TextEdit, TableWidget)

from app.common.keyboard import Keyboard


class BotWorker(QThread):
    stop_signal = Signal()
    output_signal = Signal(dict)

    def __init__(self):
        super().__init__()
        self.camera = d3dshot.create()
        self.region = (0, 0, 16, 16)
        self.stop_signal.connect(self.handle_stop)
        self.color_to_macro = None
        self.keyboard = None

    def setup(self, color_to_macro):
        self.color_to_macro = color_to_macro
        self.keyboard = Keyboard()
        if not self.keyboard.find_window("魔兽世界"):
            self.output_signal.emit({"error": f"未找到魔兽世界窗口"})
            raise ValueError("未找到魔兽世界窗口")

    def run(self):
        self.camera.capture(target_fps=6, region=self.region)
        while self.camera.is_capturing:
            time.sleep(random.uniform(0.15, 0.2))
            img = self.camera.get_latest_frame()
            if img is None:
                self.output_signal.emit({"error": f"未捕获到图像"})
                continue
            # img = self.camera.screenshot(region=self.region)
            pixels = list(img.getdata())
            unique_colors = set(pixels)
            if len(unique_colors) != 1:
                self.output_signal.emit({"error": f"颜色复杂度：{len(unique_colors)}"})
            else:
                pixel_color = pixels[0]
                macro = self.color_to_macro.get(pixel_color, None)
                if macro is not None:
                    macro["color"] = pixel_color
                    self.keyboard.send_hot_key(macro["key"])
                    self.output_signal.emit(macro)
                else:
                    self.output_signal.emit({
                        "error": f"未找到颜色：{str(pixel_color)}"
                    })

        self.output_signal.emit({"error": f"捕获已完全停止"})

    def handle_stop(self):
        self.camera.stop()


class ColorSquareWidget(QWidget):
    def __init__(self, color=(255, 0, 0), size=200, parent=None):
        """
        初始化 ColorSquareWidget 类的实例。

        :param color: 正方形的颜色，默认为红色 (255, 0, 0)
        :param size: 正方形的边长，默认为 200 像素
        """
        super().__init__(parent=parent)
        # 设置正方形的颜色
        self.color = color
        # 设置正方形的固定大小
        self.setFixedSize(size, size)

    def paintEvent(self, event):
        """
        重写 paintEvent 方法，用于绘制正方形。

        :param event: 绘制事件
        """
        # 创建一个 QPainter 对象
        painter = QPainter(self)
        # 设置画笔的颜色
        painter.setBrush(QColor(*self.color))

        painter.setPen(QPen(Qt.NoPen))
        # 绘制一个矩形，填充整个窗口
        painter.drawRect(self.rect())

    def set_size(self, width, height):
        """
        设置正方形的大小。

        :param width: 正方形的宽度
        :param height: 正方形的高度
        """
        # 设置正方形的固定大小
        self.setFixedSize(width, height)

    def set_color(self, color):
        """
        设置正方形的颜色。

        :param color: 正方形的颜色
        """
        # 更新正方形的颜色
        self.color = color
        # 调用 update 方法，触发重绘
        self.update()


class CenteredColorSquareWidget(QWidget):
    def __init__(self, color=(255, 0, 0), size=24):
        super().__init__()
        self.color_square = ColorSquareWidget(color=color, size=size)

        # 创建一个水平布局将 ColorSquareWidget 居中
        layout = QHBoxLayout()
        layout.addWidget(self.color_square, alignment=Qt.AlignCenter)
        layout.setAlignment(Qt.AlignCenter)  # 设置布局本身也居中
        self.setLayout(layout)


class RunningInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.view = QWidget(self)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("Running")

        self.vBoxLayout = QVBoxLayout(self.view)
        self.L1Layout = QHBoxLayout(self.view)
        self.L2Layout = QHBoxLayout(self.view)
        self.L3Layout = QHBoxLayout(self.view)
        self.vBoxLayout.addLayout(self.L1Layout)
        self.vBoxLayout.addLayout(self.L2Layout)
        self.vBoxLayout.addLayout(self.L3Layout)
        self.vBoxLayout.addStretch(1)
        self.L1aLayout = QVBoxLayout(self.view)
        self.L1bLayout = QVBoxLayout(self.view)
        self.L1cLayout = QVBoxLayout(self.view)
        self.L1dLayout = QVBoxLayout(self.view)
        self.L1eLayout = QVBoxLayout(self.view)
        self.L1fLayout = QVBoxLayout(self.view)
        self.L1Layout.addLayout(self.L1aLayout, 1)
        self.L1Layout.addLayout(self.L1bLayout, 1)
        self.L1Layout.addLayout(self.L1cLayout, 1)
        self.L1Layout.addLayout(self.L1dLayout, 1)
        self.L1Layout.addLayout(self.L1eLayout, 1)
        self.L1Layout.addLayout(self.L1fLayout, 1)

        self.loadKeyMapButton = PushButton(FluentIcon.DOCUMENT, "加载键位映射表", self.view)
        self.loadKeyMapButton.setDisabled(True)
        self.loadKeyMapButton.clicked.connect(self.load_key_map)
        self.currentProfileEdit = BodyLabel("还未加载配置", self.view)
        self.currentProfileEdit.setAlignment(Qt.AlignCenter)
        self.L1aLayout.addWidget(self.loadKeyMapButton)
        self.L1aLayout.addWidget(self.currentProfileEdit)

        self.nowColorLabel = BodyLabel("当前颜色", self.view)
        self.nowColorLabel.setAlignment(Qt.AlignCenter)
        self.nowColorEdit = ColorSquareWidget(color=(0, 0, 0), size=24, parent=self.view)
        self.L1bLayout.addWidget(self.nowColorLabel)
        self.L1bLayout.addWidget(self.nowColorEdit)
        self.L1bLayout.setAlignment(self.nowColorEdit, Qt.AlignHCenter)

        self.nowSkillLabel = BodyLabel("当前技能", self.view)
        self.nowSkillLabel.setAlignment(Qt.AlignCenter)
        self.nowSkillEdit = BodyLabel("还未加载配置", self.view)
        self.nowSkillEdit.setAlignment(Qt.AlignCenter)
        self.L1cLayout.addWidget(self.nowSkillLabel)
        self.L1cLayout.addWidget(self.nowSkillEdit)

        self.nowHotKeyLabel = BodyLabel("当前热键", self.view)
        self.nowHotKeyLabel.setAlignment(Qt.AlignCenter)
        self.nowHotKeyEdit = BodyLabel("还未加载配置", self.view)
        self.nowHotKeyEdit.setAlignment(Qt.AlignCenter)
        self.L1dLayout.addWidget(self.nowHotKeyLabel)
        self.L1dLayout.addWidget(self.nowHotKeyEdit)

        self.nowStatusLabel = BodyLabel("当前状态", self.view)
        self.nowStatusLabel.setAlignment(Qt.AlignCenter)
        self.nowStatusEdit = BodyLabel("还未加载配置", self.view)
        self.nowStatusEdit.setAlignment(Qt.AlignCenter)

        self.L1eLayout.addWidget(self.nowStatusLabel)
        self.L1eLayout.addWidget(self.nowStatusEdit)

        self.startBotButton = PrimaryPushButton(FluentIcon.PLAY, "开始", self.view)
        self.startBotButton.setDisabled(True)
        self.startBotButton.clicked.connect(self.start_bot)
        self.stopBotButton = PushButton(FluentIcon.PAUSE, "停止", self.view)
        self.stopBotButton.setDisabled(True)
        self.stopBotButton.clicked.connect(self.stop_bot)
        self.L1fLayout.addWidget(self.startBotButton)
        self.L1fLayout.addWidget(self.stopBotButton)

        self.color_to_macro = {}

        self.macro_table = TableWidget(self)
        self.macro_table.setColumnCount(4)
        self.macro_table.setBorderVisible(True)
        self.macro_table.setBorderRadius(8)
        self.macro_table.setWordWrap(False)
        self.macro_table.setHorizontalHeaderLabels(['宏名称', '颜色', '快捷键', '宏内容'])
        self.macro_table.verticalHeader().hide()
        self.macro_table.resizeColumnsToContents()
        self.macro_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.macro_table.setSortingEnabled(True)

        self.L2Layout.addWidget(self.macro_table, 1)

        self.log_text_edit = TextEdit(self.view)
        self.log_text_edit.setReadOnly(True)
        self.max_lines = 1000
        self.log_text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # self.log_text_edit.resize(1200, 750)
        self.L2Layout.addWidget(self.log_text_edit, 1)

        self.enableTransparentBackground()

        self.worker = BotWorker()
        self.worker.output_signal.connect(self.handle_output)

    @staticmethod
    def get_current_time():
        """获取当前时间（小时:分钟:秒.毫秒）"""
        now = datetime.now()
        return now.strftime("%H:%M:%S.%f")[:-3]  # 只保留毫秒部分

    def add_log(self, text):
        """添加日志信息，格式为 '时:分:秒.毫秒 - 日志内容'"""
        current_time = self.get_current_time()
        log_message = f"{current_time} - {text}"
        self.log_text_edit.append(log_message)

        lines = self.log_text_edit.toPlainText().splitlines()
        if len(lines) > self.max_lines:
            excess_lines = len(lines) - self.max_lines
            new_text = '\n'.join(lines[excess_lines:])
            self.log_text_edit.setPlainText(new_text)

        cursor = self.log_text_edit.textCursor()
        cursor.movePosition(QTextCursor.End)
        self.log_text_edit.setTextCursor(cursor)

    def start_bot(self):
        self.worker.setup(color_to_macro=self.color_to_macro)
        self.worker.start()
        self.startBotButton.setDisabled(True)
        self.stopBotButton.setEnabled(True)

    def stop_bot(self):
        self.worker.stop_signal.emit()

        self.startBotButton.setEnabled(True)
        self.stopBotButton.setDisabled(True)

    def onActivated(self):
        window = self.window()
        if window.profile_name is not None:
            self.currentProfileEdit.setText(window.profile_name)
            self.loadKeyMapButton.setEnabled(True)

    def load_key_map(self):
        window = self.window()
        profile = window.profile
        self.color_to_macro = {(255, 255, 255): {"title": "空闲",
                                                 "key": "无",
                                                 "code": "无"}}
        table_info = []

        for macro_name, macro_data in profile["macros"].items():
            # print(macro_name, macro_data)
            if macro_data["used"]:
                r, g, b = macro_data["color"].split(",")
                color = (int(r), int(g), int(b))
                self.color_to_macro[color] = {"title": macro_name,
                                              "key": macro_data["key"],
                                              "code": macro_data["code"]}
                table_info.append([macro_name, color, macro_data["key"], macro_data["code"]])

        self.macro_table.setRowCount(len(table_info))
        for i, row in enumerate(table_info):
            item0 = QTableWidgetItem(row[0])
            item0.setTextAlignment(Qt.AlignHCenter)
            self.macro_table.setItem(i, 0, item0)
            color = row[1]
            color_widget = CenteredColorSquareWidget(color, size=24)
            self.macro_table.setCellWidget(i, 1, color_widget)
            item2 = QTableWidgetItem(row[2])
            item2.setTextAlignment(Qt.AlignHCenter)
            self.macro_table.setItem(i, 2, item2)
            self.macro_table.setItem(i, 3, QTableWidgetItem(row[3]))

        self.macro_table.resizeRowsToContents()
        # self.macro_table.resizeColumnsToContents()
        total_height = sum(self.macro_table.rowHeight(row) for row in range(self.macro_table.rowCount()))
        total_height = total_height + self.macro_table.horizontalHeader().height() + 2
        self.macro_table.setFixedHeight(total_height)
        self.log_text_edit.setFixedHeight(total_height)
        self.startBotButton.setEnabled(True)

    def handle_output(self, output):
        if "error" in output:
            self.add_log(output["error"])
            self.nowStatusEdit.setText("错误")
        else:
            color = output["color"]
            self.nowColorEdit.set_color(color)
            if color in self.color_to_macro:
                macro_data = self.color_to_macro[color]
                self.nowSkillEdit.setText(macro_data["title"])
                self.nowHotKeyEdit.setText(macro_data["key"])
                self.nowStatusEdit.setText("正常")
                self.add_log(f"执行宏：{macro_data['title']}")
            else:
                self.nowSkillEdit.setText("未找到")
                self.add_log("未找到color " + str(color))
