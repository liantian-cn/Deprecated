# coding:utf-8
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QHBoxLayout, QVBoxLayout, QWidget)
from qfluentwidgets import (SimpleCardWidget, ScrollArea, Dialog, HorizontalSeparator, LineEdit,
                            TextEdit, IconWidget, FluentIcon, PushButton, BodyLabel, ComboBox)

from app.common.SyntaxHighlight import CommonHighlighter
# from app.common.config import save_snippet, load_snippet, list_snippets
from app.common.github import list_cloud_profile, get_cloud_profile, save_cloud_profile


class EditCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBorderRadius(8)
        self.vBoxLayout = QVBoxLayout(self)

        self.cloudIconLabel = IconWidget(FluentIcon.CLOUD, self)
        self.cloudIconLabel.setFixedSize(24, 24)
        self.cloudComboBox = ComboBox(self)
        self.cloudRefreshButton = PushButton(FluentIcon.UPDATE, "刷新云端列表", self)
        self.cloudRefreshButton.clicked.connect(self.refresh_cloud_list)
        self.cloudLoadButton = PushButton(FluentIcon.CLOUD_DOWNLOAD, "云端读取", self)
        self.cloudLoadButton.clicked.connect(self.load_snippet_cloud)
        # self.cloudSaveButton = PushButton(FluentIcon.SAVE, "保存到云端", self)
        # self.cloudSaveButton.clicked.connect(self.save_snippet_cloud)

        self.profileToCloudButton = PushButton(FluentIcon.IMAGE_EXPORT, "将当前配置文件所有属性保存到云端", self)
        self.profileToCloudButton.clicked.connect(self.save_profile_to_cloud)

        self.codeEdit = TextEdit(self)
        self.codeEdit.textChanged.connect(self.adjust_height)
        self.codeEdit.highlighter = CommonHighlighter(self.codeEdit.document())

        self.argsInput = LineEdit(self)
        self.argsInput.setPlaceholderText("输入参数，多个参数用英文逗号隔开")

        self.descriptionEdit = LineEdit(self)
        self.descriptionEdit.setPlaceholderText("输入描述信息，便于以后查看，可为空")

        help_text = ("说明文档：\n"
                     "这里用来保存一些常用的代码片段，方便使用。\n"
                     "检测失败的行，可以在末尾加上 -- luacheck: ignore\n")
        self.helpLabel = BodyLabel(help_text, self)
        self.helpLabel.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.helpLabel.setWordWrap(True)

        self.L1Layout = QHBoxLayout()
        self.L2Layout = QHBoxLayout()
        self.L3Layout = QHBoxLayout()
        self.L4Layout = QHBoxLayout()
        self.L5Layout = QHBoxLayout()

        self.L1Layout.addWidget(self.profileToCloudButton, 1)

        self.L2Layout.addSpacing(8)
        self.L2Layout.addWidget(self.cloudIconLabel, 1)
        self.L2Layout.addSpacing(8)
        self.L2Layout.addWidget(self.cloudComboBox, 2)
        self.L2Layout.addWidget(self.cloudRefreshButton, 1)
        self.L2Layout.addWidget(self.cloudLoadButton, 1)
        # self.L2Layout.addWidget(self.cloudSaveButton, 1)

        self.L3Layout.addWidget(self.argsInput, 5)
        self.L3Layout.addWidget(self.descriptionEdit, 5)

        self.L4Layout.addWidget(self.codeEdit, 1)

        self.L5Layout.addWidget(self.helpLabel, 10)

        self.vBoxLayout.addLayout(self.L1Layout)
        self.vBoxLayout.addLayout(self.L2Layout)
        self.vBoxLayout.addWidget(HorizontalSeparator(self))
        self.vBoxLayout.addLayout(self.L3Layout)
        self.vBoxLayout.addLayout(self.L4Layout)
        self.vBoxLayout.addWidget(HorizontalSeparator(self))
        self.vBoxLayout.addLayout(self.L5Layout)

    def adjust_height(self):
        # self.contentEdit.setFixedHeight(int(self.contentEdit.document().size().height() + 20))
        height = len(self.codeEdit.toPlainText().splitlines()) * 19 + 40
        self.codeEdit.setFixedHeight(max(60, height))

    def show_error(self, title, error):
        w = Dialog(title, error, self)
        w.yesButton.setText("我知道了")
        w.cancelButton.hide()
        w.buttonLayout.insertStretch(1)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')

    def set_all_button(self, state):
        self.cloudLoadButton.setEnabled(state)
        # self.cloudSaveButton.setEnabled(state)
        self.cloudRefreshButton.setEnabled(state)

    def refresh_cloud_list(self):
        self.set_all_button(False)
        self.cloudComboBox.clear()
        self.cloudComboBox.addItems(list_cloud_profile(path="snippets/"))
        self.cloudComboBox.setCurrentIndex(-1)
        self.set_all_button(True)

    def save_profile_to_cloud(self):
        self.set_all_button(False)
        window = self.window()
        username = window.username

        profile = window.profile
        properties = profile.get("properties", {})
        for k, v in properties.items():
            if v["used"]:
                data = {key: v[key] for key in ["code", "desc", "func_args"] if key in v}
                save_cloud_profile(f"{k}@{username}", data, path="snippets/")
        self.set_all_button(True)
        return self.show_error("提示", "保存成功")


    def load_snippet_cloud(self):
        self.set_all_button(False)
        snippet_name = self.cloudComboBox.currentText()
        if snippet_name.strip() == "":
            self.set_all_button(True)
            return self.show_error("有点问题", "请选择一个配置，没有点刷新")
        try:
            data = get_cloud_profile(snippet_name, path="snippets/")
            self.codeEdit.setPlainText(data["code"])
            self.argsInput.setText(",".join(data["func_args"]))
            self.descriptionEdit.setText(data["desc"])
            self.set_all_button(True)
            return self.show_error("提示", "读取成功")
        except Exception as e:
            self.set_all_button(True)
            return self.show_error("云读取失败", e)


class SnippetInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.view = QWidget(self)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("SnippetInterface")

        self.vBoxLayout = QVBoxLayout(self.view)

        self.editCard = EditCard(self)

        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.editCard, 0, Qt.AlignTop)
        self.enableTransparentBackground()

    def onActivated(self):
        self.editCard.refresh_cloud_list()
