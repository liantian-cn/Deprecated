# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout, QVBoxLayout, QWidget, QSizePolicy)
from qfluentwidgets import (BodyLabel, SimpleCardWidget, TitleLabel, ScrollArea, Dialog, LineEdit, PushButton, TextEdit,
                            ComboBox)

from app.common.SyntaxHighlight import CommonHighlighter
from app.common.utils import (check_lua_code, putty_code,
                              generate_unique_strings, remove_random_element, parse_key_arguments)


class PropertyCard(SimpleCardWidget):
    def __init__(self, property, parent=None):
        super().__init__(parent)
        self.setBorderRadius(8)
        self.title = property["title"]

        # pprint.pprint(property)

        self.titleLabel = BodyLabel("属性名称：", self)
        self.titleInput = BodyLabel(property["title"], self)
        # print(property["title"])
        self.titleInput.setTextInteractionFlags(Qt.TextSelectableByMouse)

        self.countLabel = BodyLabel("当前Rotation中出现次数：", self)
        self.countInput = BodyLabel(str(property["count"]), self)

        self.descriptionLabel = BodyLabel("描述：", self)
        self.descriptionEdit = LineEdit(self)
        self.descriptionEdit.setPlaceholderText("输入描述信息，便于以后查看，可为空")
        self.origin_description = property["desc"]
        self.descriptionEdit.setText(self.origin_description)

        self.currArgsLabel = BodyLabel("当前Rotation中参数：", self)
        self.currArgsInput = ComboBox(self)

        for arg in property["args"]:
            if arg:
                self.currArgsInput.addItem(str(arg))

        self.argsLabel = BodyLabel("参数：", self)
        self.argsInput = LineEdit(self)
        self.argsInput.setPlaceholderText("输入参数，多个参数用英文逗号隔开")
        self.origin_args = ",".join(property["func_args"])
        self.argsInput.setText(self.origin_args)

        # self.importLabel = BodyLabel("快捷导入", self)
        # self.importBox = ComboBox(self)
        # self.importButton = PushButton("导入", self)

        self.check_button = PushButton("代码检查", self)
        self.check_button.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Expanding)
        self.check_button.clicked.connect(lambda: self.check_code(False))

        self.origin_code = property["code"]
        self.codeEdit = TextEdit(self)
        self.codeEdit.setPlainText(self.origin_code)

        # print(f">>>>>>\n\n\n\n{self.origin_code}\n\n\n\n<<<<<<\n")

        self.codeEdit.textChanged.connect(self.adjust_height)
        self.codeEdit.highlighter = CommonHighlighter(self.codeEdit.document())

        self.vBoxLayout = QVBoxLayout(self)

        self.L1Layout = QHBoxLayout(self)
        self.L2Layout = QHBoxLayout(self)
        self.L3Layout = QHBoxLayout(self)

        self.L1Layout.addWidget(self.titleLabel, 1, Qt.AlignRight)
        self.L1Layout.addWidget(self.titleInput, 1)

        self.L1Layout.addWidget(self.countLabel, 1, Qt.AlignRight)
        self.L1Layout.addWidget(self.countInput, 1)

        self.L1Layout.addWidget(self.currArgsLabel, 1, Qt.AlignRight)
        self.L1Layout.addWidget(self.currArgsInput, 1)

        self.L2Layout.addWidget(self.argsLabel, 1, Qt.AlignRight)
        self.L2Layout.addWidget(self.argsInput, 2)
        self.L2Layout.addWidget(self.descriptionLabel, 1, Qt.AlignRight)
        self.L2Layout.addWidget(self.descriptionEdit, 2)
        # self.L2Layout.addWidget(self.importLabel, 1, Qt.AlignRight)
        # self.L2Layout.addWidget(self.importBox, 1)
        # self.L2Layout.addWidget(self.importButton, 1)

        self.L3Layout.addWidget(self.check_button, 1)
        self.L3Layout.addWidget(self.codeEdit, 6)

        # self.vBoxLayout.addLayout(self.titleLayout)
        # self.vBoxLayout.addLayout(self.countLayout)
        self.vBoxLayout.addLayout(self.L1Layout)
        self.vBoxLayout.addLayout(self.L2Layout)
        self.vBoxLayout.addLayout(self.L3Layout)

    def adjust_height(self):
        height = len(self.codeEdit.toPlainText().splitlines()) * 19 + 20
        self.codeEdit.setFixedHeight(max(60, height))

    def check_load_profile(self):
        return (self.codeEdit.toPlainText() == self.origin_code) and (
                self.descriptionEdit.text() == self.origin_description) and (
                self.argsInput.text() == self.origin_args)

    def save_profile(self):
        self.origin_description = self.descriptionEdit.text()
        self.origin_code = self.codeEdit.toPlainText()
        self.origin_args = self.argsInput.text()
        func_args = self.argsInput.text().strip().split(",")
        if func_args == [""]:
            func_args = []
        return {
            "title": self.title,
            "description": self.descriptionEdit.text(),
            "code": self.codeEdit.toPlainText(),
            "func_args": func_args,
        }

    def check_code(self, silent=True):
        code = self.codeEdit.toPlainText()
        code = putty_code(code)
        self.codeEdit.setPlainText(code)

        if code == "":
            w = Dialog("提示", "你好像什么都没写", self)
            w.yesButton.setText("我知道了")
            w.cancelButton.hide()
            w.buttonLayout.insertStretch(1)
            if w.exec():
                return True
        func_args = self.argsInput.text().strip().split(",")
        full_code = f"local function test ({','.join(func_args)})\n{code}\nend"

        error = check_lua_code(full_code)
        print(full_code)
        print(error)
        if silent:
            if error.strip() == "":
                return True
            else:
                raise ValueError(f"Prop {self.title} 的代码块异常。错误信息{error}")
        else:
            if error.strip() == "":
                w = Dialog("提示", "代码正常，但以游戏为准", self)
                w.yesButton.setText("我知道了")
                w.cancelButton.hide()
                w.buttonLayout.insertStretch(1)
                if w.exec():
                    return True
            else:
                w = Dialog("错误", error, self)
                w.yesButton.setText("我知道了")
                w.cancelButton.hide()
                w.buttonLayout.insertStretch(1)
                if w.exec():
                    return True


class PropertyInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.view = QWidget(self)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("PropertyInterface")

        self.vBoxLayout = QVBoxLayout(self.view)

        self.titleLabel = TitleLabel(self)
        self.titleLabel.setText("属性设置")

        self.descriptionLabel = BodyLabel(self)
        self.descriptionLabel.setText('属性为脚本中可以通过Prop()函数调用的代码片段，要有一个返回值')
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

    def clear_cards(self):
        for card in self.cards:
            self.cardLayout.removeWidget(card)
            card.deleteLater()
        self.cards = []

    def load_profile(self, profile):
        self.clear_cards()
        profile_props = profile.get("properties", {})
        rotation_text = profile.get("rotation", "")
        # rotation_props = generate_count_dict(extract_prop_arguments(rotation_text, "Prop"))
        # print(rotation_props)
        rotation_props2 = parse_key_arguments(rotation_text, "Prop")
        # print(rotation_props2)
        # for prop in rotation_props:
        #     prop["title"] = prop["string"]

        for prop in rotation_props2:
            saved_prop = profile_props.get(prop["title"], None)
            # print(saved_prop)
            if saved_prop is None:
                prop["code"] = ""
                prop["desc"] = ""
                prop["func_args"] = []
            else:
                prop["code"] = saved_prop.get("code", "")
                prop["desc"] = saved_prop.get("desc", "")
                prop["func_args"] = saved_prop.get("func_args", [])
        # print(rotation_props2)
        for prop in rotation_props2:
            card = PropertyCard(prop, parent=self)
            # card.countInput.setText(str(prop["count"]))
            self.cardLayout.addWidget(card)
            self.cards.append(card)

    def save_profile(self, profile):
        properties = profile.get("properties", {})
        for k, v in properties.items():
            properties[k]["used"] = False

        string_list = generate_unique_strings(len(self.cards), 8)

        for card in self.cards:
            card_info = card.save_profile()
            # var_name = remove_random_element(string_list)
            func_name = f"p_{remove_random_element(string_list)}"
            properties[card_info["title"]] = {
                "code": card_info["code"],
                "desc": card_info["description"],
                "func_args": card_info["func_args"],
                "used": True,
                "func_name": func_name,
            }
        profile["properties"] = properties

        return profile

    def onActivated(self):
        pass
