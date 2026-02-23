# coding:utf-8

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout)
from PySide6.QtWidgets import (QVBoxLayout, QWidget)
from qfluentwidgets import (BodyLabel, SimpleCardWidget, ScrollArea, Dialog, HorizontalSeparator)
from qfluentwidgets import (PlainTextEdit)
from qfluentwidgets import (PrimaryPushButton)

from app.common import config


class EditCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBorderRadius(8)
        self.vBoxLayout = QVBoxLayout(self)

        # "interrupt_spell_list": [],
        # "interrupt_black_list": [],
        # "important_spell_list": []

        self.interruptSpellListLabel = BodyLabel("打断法术列表：", self)
        self.interruptSpellListInput = PlainTextEdit(self)
        self.interruptSpellListInput.setPlaceholderText("输入打断法术列表，多个法术用英文逗号隔开")

        self.interruptBlackListLabel = BodyLabel("打断黑名单：", self)
        self.interruptBlackListInput = PlainTextEdit(self)
        self.interruptBlackListInput.setPlaceholderText("输入打断黑名单，多个法术用英文逗号隔开")

        self.importantSpellListLabel = BodyLabel("重要法术列表：", self)
        self.importantSpellListInput = PlainTextEdit(self)
        self.importantSpellListInput.setPlaceholderText("输入重要法术列表，多个法术用英文逗号隔开")

        self.saveButton = PrimaryPushButton("保存", self)
        self.saveButton.clicked.connect(self.save_config)

        self.manualText = BodyLabel("说明：", self)
        self.manualText.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.manualText.setWordWrap(True)
        self.manualText.setText("说明文档：\n"
                                "0. 所有技能ID都是数字。\n"
                                "1. 使用PixelRotationLT.CanInterrupt(target)判断是否可以打断。黑名单生效。\n"
                                "2. 使用PixelRotationLT.ShouldInterrupt(target)判断目标施法是否需要打断。黑名单和白名单都生效。\n"
                                "3. 使用EnemiesIsImportantSpell()判断周围有没有敌人在释放危险技能。不一定是主目标。\n")

        self.L1Layout = QHBoxLayout()
        self.L2Layout = QHBoxLayout()
        self.L3Layout = QHBoxLayout()
        self.L4Layout = QHBoxLayout()
        self.L5Layout = QHBoxLayout()

        self.L1Layout.addWidget(self.interruptSpellListLabel, 1)
        self.L1Layout.addWidget(self.interruptSpellListInput, 4)

        self.L2Layout.addWidget(self.interruptBlackListLabel, 1)
        self.L2Layout.addWidget(self.interruptBlackListInput, 4)

        self.L3Layout.addWidget(self.importantSpellListLabel, 1)
        self.L3Layout.addWidget(self.importantSpellListInput, 4)
        self.L4Layout.addWidget(self.manualText, 9)
        self.L4Layout.addWidget(self.saveButton, 1)

        self.vBoxLayout.addLayout(self.L1Layout)
        self.vBoxLayout.addWidget(HorizontalSeparator(self))
        self.vBoxLayout.addLayout(self.L2Layout)
        self.vBoxLayout.addWidget(HorizontalSeparator(self))
        self.vBoxLayout.addLayout(self.L3Layout)
        self.vBoxLayout.addWidget(HorizontalSeparator(self))
        self.vBoxLayout.addLayout(self.L4Layout)

    def show_error(self, title, error):
        w = Dialog(title, error, self)
        w.yesButton.setText("我知道了")
        w.cancelButton.hide()
        w.buttonLayout.insertStretch(1)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')

    @staticmethod
    def check_input(self, text):
        # 检测字符串用逗号分割后，是不是都是数字。
        if text == '':
            return True
        for spell in text.split(','):
            if not spell.strip().isdigit():
                return False
        return True

    def load_config(self):
        self.interruptSpellListInput.setPlainText(', '.join(config.load_value("interrupt_spell_list", [])))
        self.interruptBlackListInput.setPlainText(', '.join(config.load_value("interrupt_black_list", [])))
        self.importantSpellListInput.setPlainText(', '.join(config.load_value("important_spell_list", [])))

    def save_config(self):
        if not self.check_input(self, self.interruptSpellListInput.toPlainText()):
            return self.show_error("输入错误", "打断法术列表输入错误")
        if not self.check_input(self, self.interruptBlackListInput.toPlainText()):
            return self.show_error("输入错误", "打断黑名单输入错误")
        if not self.check_input(self, self.importantSpellListInput.toPlainText()):
            return self.show_error("输入错误", "重要法术列表输入错误")

        interrupt_spell_list = self.interruptSpellListInput.toPlainText().split(',')
        interrupt_spell_list = [spell.strip() for spell in interrupt_spell_list if spell.strip()]
        interrupt_spell_list = list(set(interrupt_spell_list))
        config.save_key_value("interrupt_spell_list", interrupt_spell_list)

        interrupt_black_list = self.interruptBlackListInput.toPlainText().split(',')
        interrupt_black_list = [spell.strip() for spell in interrupt_black_list if spell.strip()]
        interrupt_black_list = list(set(interrupt_black_list))
        config.save_key_value("interrupt_black_list", interrupt_black_list)

        important_spell_list = self.importantSpellListInput.toPlainText().split(',')
        important_spell_list = [spell.strip() for spell in important_spell_list if spell.strip()]
        important_spell_list = list(set(important_spell_list))
        config.save_key_value("important_spell_list", important_spell_list)


class PublicFuncInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.view = QWidget(self)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("PublicFuncInterface")

        self.vBoxLayout = QVBoxLayout(self.view)

        self.editCard = EditCard(self)

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.editCard, 0, Qt.AlignTop)
        self.enableTransparentBackground()

    def onActivated(self):
        self.editCard.load_config()
