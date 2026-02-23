# coding:utf-8

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout, QVBoxLayout, QWidget)
from qfluentwidgets import (BodyLabel, SimpleCardWidget, TitleLabel, ScrollArea, Dialog, LineEdit, TextEdit)

from app.common.dataset import MACRO_KEY_LIST, MACRO_COLOR_LIST
from app.common.utils import (extract_prop_arguments, generate_count_dict, remove_random_element,
                              generate_unique_strings)


class MacroCard(SimpleCardWidget):
    def __init__(self, title, macro_string, description, parent=None):
        super().__init__(parent)
        self.setBorderRadius(8)
        self.title = title

        self.titleLabel = BodyLabel("宏名称：", self)
        self.titleInput = BodyLabel(title, self)
        self.titleInput.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.countLabel = BodyLabel("当前Rotation中出现次数：", self)
        self.countInput = BodyLabel("10", self)

        self.descriptionLabel = BodyLabel("描述：", self)
        self.descriptionEdit = LineEdit(self)
        self.descriptionEdit.setPlaceholderText("输入描述信息，便于以后查看，可为空")
        self.origin_description = description
        self.descriptionEdit.setText(description)

        self.keyLabel = BodyLabel("快捷键：", self)
        self.keyEdit = BodyLabel("", self)

        self.colorLabel = BodyLabel("颜色：", self)
        self.colorEdit = BodyLabel("", self)
        self.color = ""

        self.macroLabel = BodyLabel("宏命令：", self)
        self.macroEdit = TextEdit(self)
        self.origin_macro = macro_string
        self.macroEdit.textChanged.connect(self.adjust_height)
        self.macroEdit.setPlainText(macro_string)
        # self.macroEdit.highlighter = CommonHighlighter(self.codeEdit.document())

        self.vBoxLayout = QVBoxLayout(self)

        self.L1Layout = QHBoxLayout(self)
        self.L2Layout = QHBoxLayout(self)
        self.L3Layout = QHBoxLayout(self)

        self.L1Layout.addWidget(self.titleLabel, 1, Qt.AlignRight)
        self.L1Layout.addWidget(self.titleInput, 2)

        self.L1Layout.addWidget(self.countLabel, 1, Qt.AlignRight)
        self.L1Layout.addWidget(self.countInput, 2)

        self.L2Layout.addWidget(self.keyLabel, 1, Qt.AlignRight)
        self.L2Layout.addWidget(self.keyEdit, 2)

        self.L2Layout.addWidget(self.colorLabel, 1, Qt.AlignRight)
        self.L2Layout.addWidget(self.colorEdit, 2)

        self.L3Layout.addWidget(self.descriptionLabel, 1, Qt.AlignRight)
        self.L3Layout.addWidget(self.descriptionEdit, 5)

        self.codeLayout = QHBoxLayout(self)
        self.codeLayout.addWidget(self.macroLabel, 1, Qt.AlignRight)
        self.codeLayout.addWidget(self.macroEdit, 5)

        self.vBoxLayout.addLayout(self.L1Layout)
        self.vBoxLayout.addLayout(self.L2Layout)
        self.vBoxLayout.addLayout(self.L3Layout)
        self.vBoxLayout.addLayout(self.codeLayout)

    def setColor(self, color):
        try:
            r, g, b = color
        except:
            r, g, b = color.split(',')
        self.colorEdit.setStyleSheet(f"background-color: rgb({r}, {g}, {b});")
        self.colorEdit.setText(f"RGB({r},{g},{b})")
        self.color = f"{r},{g},{b}"

    def adjust_height(self):
        height = len(self.macroEdit.toPlainText().splitlines()) * 20 + 20
        self.macroEdit.setFixedHeight(max(40, height))

    def check_load_profile(self):
        return (self.macroEdit.toPlainText() == self.origin_macro) and (
                self.descriptionEdit.text() == self.origin_description)

    def save_profile(self):
        self.origin_description = self.descriptionEdit.text()
        self.origin_macro = self.macroEdit.toPlainText()
        return {
            "title": self.title,
            "description": self.descriptionEdit.text(),
            "code": self.macroEdit.toPlainText(),
            'color': self.color,
            'key': self.keyEdit.text(),
        }


class MacroInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.view = QWidget(self)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("MacroInterface")

        self.vBoxLayout = QVBoxLayout(self.view)

        self.titleLabel = TitleLabel(self)
        self.titleLabel.setText("宏设置")

        self.descriptionLabel = BodyLabel(self)
        self.descriptionLabel.setText('所有操作都通过宏来完成，在这里为所有Cast对象设置宏命令')
        self.descriptionLabel.setWordWrap(True)

        self.vBoxLayout.addWidget(self.titleLabel)
        self.vBoxLayout.addWidget(self.descriptionLabel)
        self.vBoxLayout.addSpacing(8)

        self.vBoxLayout.setSpacing(10)
        self.enableTransparentBackground()

        self.cardLayout = QVBoxLayout(self.view)
        self.cardLayout.setSpacing(0)
        self.cardLayout.setContentsMargins(0, 0, 0, 0)
        self.vBoxLayout.addLayout(self.cardLayout)

        self.cards = []

        self.vBoxLayout.addStretch(1)

    def clear_cards(self):
        for card in self.cards:
            self.cardLayout.removeWidget(card)
            card.deleteLater()
        self.cards = []

    def check_load_profile(self, profile):
        result = True
        for card in self.cards:
            if not card.check_load_profile():
                result = False
        if not result:
            w = Dialog("警告", "有属性设置未保存，继续么？", self)
            w.yesButton.setText("我知道了")
            w.cancelButton.setText("阻止加载")
            w.buttonLayout.insertStretch(1)
            if w.exec():
                return True
            else:
                return False
        return result

    def load_profile(self, profile):
        self.clear_cards()
        profile_macros = profile.get("macros", {})
        rotation_text = profile.get("rotation", "")
        rotation_macros = generate_count_dict(extract_prop_arguments(rotation_text, "Cast"))

        for macro in rotation_macros:
            macro["title"] = macro["string"]

        for macro in rotation_macros:
            saved_macro = profile_macros.get(macro["string"], None)
            if saved_macro is None:
                macro["code"] = ""
                macro["desc"] = ""
            else:
                macro["code"] = saved_macro.get("code", "")
                macro["desc"] = saved_macro.get("desc", "")
                macro["key"] = saved_macro.get("key", None)
                macro["color"] = saved_macro.get("color", None)

        # print(rotation_macros)

        for macro in rotation_macros:
            card = MacroCard(title=macro["title"],
                             macro_string=macro["code"],
                             description=macro["desc"],
                             parent=self)
            card.countInput.setText(str(macro["count"]))

            color = macro.get("color", None)
            if color is not None:
                card.setColor(color)
            key = macro.get("key", None)
            if key is not None:
                card.keyEdit.setText(key)

            self.cardLayout.addWidget(card)
            self.cards.append(card)

    def save_profile(self, profile):
        profile_macros = profile.get("macros", {})
        for k, v in profile_macros.items():
            profile_macros[k]["used"] = False

        key_list = MACRO_KEY_LIST.copy()
        color_list = MACRO_COLOR_LIST.copy()
        for card in self.cards:
            key = remove_random_element(key_list)
            color = remove_random_element(color_list)
            card.setColor(color)
            card.keyEdit.setText(key)
        string_list = generate_unique_strings(len(self.cards) * 3, 8)
        for card in self.cards:
            card_info = card.save_profile()
            profile_macros[card_info["title"]] = {
                "code": card_info["code"],
                "desc": card_info["description"],
                "key": card_info["key"],
                "color": card_info["color"],
                "macro_name": f"m_{remove_random_element(string_list)}",
                "frame_name": f"f_{remove_random_element(string_list)}",
                "btn_name": f"b_{remove_random_element(string_list)}",
                "used": True
            }
        profile["macros"] = profile_macros
        return profile

    def onActivated(self):
        pass
