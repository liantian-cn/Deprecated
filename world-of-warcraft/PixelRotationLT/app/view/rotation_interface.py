# coding:utf-8

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QVBoxLayout, QWidget)
from qfluentwidgets import (BodyLabel, CaptionLabel, SimpleCardWidget, ScrollArea, Dialog, HorizontalSeparator,
                            TextEdit)

from app.common.SyntaxHighlight import CommonHighlighter
from app.common.utils import putty_code, check_lua_code


class RotationEditCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBorderRadius(8)

        self.titleLayout = QVBoxLayout()
        self.titleLayout.setContentsMargins(8, 0, 8, 0)  # (左, 上, 右, 下)
        self.titleLayout.addWidget(BodyLabel("Rotation编辑", self))
        self.titleLayout.addWidget(CaptionLabel("Prop：获取属性，参数是属性栏定义的名称，例如Prop(\"自身血量\")", self))
        self.titleLayout.addWidget(CaptionLabel("Cast：运行宏，参数是宏栏定义的名称，例如Cast(\"暗影箭\")", self))
        self.titleLayout.addWidget(
            CaptionLabel("CoolDown：表示冷却时间，值单位是冷却名和冷却时间（毫秒），例如CollDown(\"日蚀\",1000)", self))
        self.titleLayout.addWidget(CaptionLabel(
            "Select：选择目标，参数是目标ID，目标ID一般通过特定的属性值获取，例如Select(Prop(\"全团血量最低\"))", self))
        self.titleLayout.addWidget(CaptionLabel("Idle：闲置发呆", self))
        self.titleLayout.addWidget(CaptionLabel("编辑完毕，要在基础设置内保存生效。", self), 0, Qt.AlignRight)

        self.title_separator = HorizontalSeparator(self)

        self.origin_content = ""
        self.contentEdit = TextEdit(self)
        self.contentEdit.textChanged.connect(self.adjust_height)
        self.contentEdit.highlighter = CommonHighlighter(self.contentEdit.document())

        self.vBoxLayout = QVBoxLayout(self)

        #

        self.vBoxLayout.addLayout(self.titleLayout)
        self.vBoxLayout.addWidget(self.title_separator)
        self.vBoxLayout.addWidget(self.contentEdit, 1)

    def adjust_height(self):
        # self.contentEdit.setFixedHeight(int(self.contentEdit.document().size().height() + 20))
        height = len(self.contentEdit.toPlainText().splitlines()) * 19 + 40
        self.contentEdit.setFixedHeight(max(60, height))

    def show_error(self, title, error):
        w = Dialog(title, error, self)
        w.yesButton.setText("我知道了")
        w.cancelButton.hide()
        w.buttonLayout.insertStretch(1)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')

    def save_profile(self, profile):
        rotation_text = self.contentEdit.toPlainText()
        rotation_text = putty_code(rotation_text)
        self.contentEdit.setPlainText(rotation_text)

        check_result = check_lua_code(rotation_text)
        if check_result.strip() != "":
            raise ValueError(f"Rotation语法检查不通过{check_result}")

        profile["rotation"] = rotation_text
        self.origin_content = rotation_text
        return profile

    def check_load_profile(self, profile):
        if self.origin_content == "":
            return True
        if self.origin_content == self.contentEdit.toPlainText():
            return True
        w = Dialog("警告", "Rotation未保存，继续么？", self)
        w.yesButton.setText("我知道了")
        w.cancelButton.setText("阻止加载")
        w.buttonLayout.insertStretch(1)
        if w.exec():
            return True
        else:
            return False

    def load_profile(self, profile):
        self.contentEdit.setPlainText(profile["rotation"])
        self.origin_content = profile["rotation"]
        self.adjust_height()


class RotationInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.view = QWidget(self)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("RotationInterface")

        self.vBoxLayout = QVBoxLayout(self.view)

        self.rotation_edit_card = RotationEditCard(self)

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.rotation_edit_card, 0, Qt.AlignTop)
        self.enableTransparentBackground()

    def load_profile(self, profile):
        self.rotation_edit_card.load_profile(profile)

    def save_profile(self, profile):
        profile = self.rotation_edit_card.save_profile(profile)
        return profile

    def check_load_profile(self, profile):
        return self.rotation_edit_card.check_load_profile(profile)

    def onActivated(self):
        pass
