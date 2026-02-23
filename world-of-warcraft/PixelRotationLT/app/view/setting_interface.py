# coding:utf-8
import base64
import pprint

from PySide6.QtCore import Qt, QUrl
from PySide6.QtGui import QColor, QImage
from PySide6.QtWidgets import (QHBoxLayout, QVBoxLayout, QWidget, QFileDialog)
from qfluentwidgets import (IconWidget, BodyLabel, CaptionLabel, ImageLabel, HeaderCardWidget, HyperlinkLabel,
                            SimpleCardWidget, PrimaryPushButton, ScrollArea, Dialog, HorizontalSeparator,
                            StrongBodyLabel, LineEdit, FluentIcon, PushButton, EditableComboBox)

from app.common import config
from app.common.github import list_cloud_profile, get_cloud_profile, save_cloud_profile
from app.common.utils import get_machine_code, get_act_code
from app.resource.logo2 import image_data as image_data_base64


class ActivationCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBorderRadius(8)

        self.machineCodeLabel = StrongBodyLabel("机器码:", self)
        self.machineCodeEdit = LineEdit(self)
        self.machine_code = get_machine_code()
        self.machineCodeEdit.setText(self.machine_code)
        self.machineCodeEdit.setReadOnly(True)

        self.usernameLabel = StrongBodyLabel("用户名:", self)
        self.usernameEdit = LineEdit(self)
        self.usernameEdit.setFixedWidth(200)

        self.actCodeLabel = StrongBodyLabel("激活码:", self)
        self.actCodeEdit = LineEdit(self)

        self.vBoxLayout = QVBoxLayout(self)

        self.machineCodeLayout = QHBoxLayout(self)
        self.machineCodeLayout.addWidget(self.machineCodeLabel)
        self.machineCodeLayout.addWidget(self.machineCodeEdit)

        self.actCodeLayout = QHBoxLayout(self)
        self.actCodeLayout.addWidget(self.usernameLabel)
        self.actCodeLayout.addWidget(self.usernameEdit)
        self.actCodeLayout.addWidget(self.actCodeLabel)
        self.actCodeLayout.addWidget(self.actCodeEdit)

        self.actButton = PrimaryPushButton(FluentIcon.DEVELOPER_TOOLS, "激活", self)
        self.actButton.clicked.connect(self.validate_activation_code)

        self.vBoxLayout.addLayout(self.machineCodeLayout)
        self.vBoxLayout.addLayout(self.actCodeLayout)
        self.vBoxLayout.addWidget(self.actButton)
        self.vBoxLayout.addStretch(1)
        self.load_code()

    def load_code(self):
        code = config.load_value("act_code")
        if code is not None:
            self.actCodeEdit.setText(code)
        username = config.load_value("username")
        if code is not None:
            self.usernameEdit.setText(username)

    def validate_activation_code(self):
        window = self.window()
        username = self.usernameEdit.text().strip()
        act_code = get_act_code(self.machine_code, username)
        # print(act_code)

        if self.actCodeEdit.text().strip() == act_code:
            config.save_key_value("act_code", self.actCodeEdit.text().strip())
            config.save_key_value("username", username)
            window.username = username
            window.activate_software()


class AppInfoCard(HeaderCardWidget):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setTitle('说明')

        self.LeftLayout = QVBoxLayout(self)
        self.RightLayout = QVBoxLayout(self)

        self.viewLayout.addLayout(self.LeftLayout, 1)
        self.viewLayout.addLayout(self.RightLayout, 1)

        self.descriptionEdit = BodyLabel(self)
        self.descriptionEdit.setText("0. 删掉PixelRotation开头的插件。\n"
                                     "1. 激活。\n"
                                     "2. 设置好游戏路径\n"
                                     "3. 选择并加载一个配置。\n"
                                     "4. 点击生成插件。\n"
                                     "5. 运行游戏。\n"
                                     "6.最后点击运行脚本")

        image_bytes = base64.b64decode(image_data_base64)
        image = QImage.fromData(image_bytes)
        self.iconLabel = ImageLabel(image, self)
        self.iconLabel.setBorderRadius(8, 8, 8, 8)
        self.iconLabel.scaledToWidth(360)

        self.discord_link = HyperlinkLabel(QUrl('https://discord.gg/hSbDh2b2'), 'Discord', self)

        self.LeftLayout.addWidget(self.iconLabel)
        self.LeftLayout.addWidget(self.discord_link)
        self.RightLayout.addWidget(self.descriptionEdit, 1, Qt.AlignLeft)

        self.setBorderRadius(8)


class GamePathCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBorderRadius(8)

        self.titleLabel = StrongBodyLabel("游戏路径设置", self)
        self.descriptionLabel = CaptionLabel("请选择_retail_目录", self)
        self.title_separator = HorizontalSeparator(self)

        self.iconLabel = IconWidget(FluentIcon.FOLDER, self)
        self.iconLabel.setFixedSize(24, 24)
        self.contentLabel = BodyLabel("", self)
        self.button = PushButton("选择文件夹", self)
        self.button.clicked.connect(self.clicked_button)

        self.vBoxLayout = QVBoxLayout(self)

        self.titleLayout = QHBoxLayout()
        self.vBoxLayout.addLayout(self.titleLayout)
        #
        self.titleLayout.setContentsMargins(8, 8, 8, 0)  # (左, 上, 右, 下)
        self.titleLayout.addWidget(self.titleLabel, 1, Qt.AlignLeft)
        self.titleLayout.addWidget(self.descriptionLabel, 1, Qt.AlignRight)

        self.vBoxLayout.addWidget(self.title_separator)

        self.settingLayout = QHBoxLayout(self)
        self.settingLayout.setAlignment(Qt.AlignVCenter)
        self.settingLayout.setSpacing(0)
        self.settingLayout.setContentsMargins(8, 8, 8, 8)

        self.vBoxLayout.addLayout(self.settingLayout)

        self.settingLayout.addWidget(self.iconLabel, 0, Qt.AlignLeft)
        self.settingLayout.addSpacing(16)
        self.settingLayout.addWidget(self.contentLabel, 0, Qt.AlignLeft)
        self.settingLayout.addStretch(1)
        self.settingLayout.addWidget(self.button, 0, Qt.AlignLeft)
        self.load_config()

    def load_config(self):
        game_path = config.load_value("GamePath")
        if game_path is not None:
            self.contentLabel.setText(game_path)

    def clicked_button(self):
        folder = QFileDialog.getExistingDirectory(
            self, "请选择目录", "./")
        if folder:
            if folder.endswith("_retail_"):
                self.contentLabel.setText(folder)
                config.save_key_value("GamePath", folder)
            else:
                w = Dialog("错误", "必须选择_retail_目录", self)
                w.yesButton.setText("我知道了")
                w.cancelButton.hide()
                w.buttonLayout.insertStretch(1)
                if w.exec():
                    print('Yes button is pressed')
                else:
                    print('Cancel button is pressed')


class RotationProfileCard(SimpleCardWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setBorderRadius(8)

        self.titleLabel = StrongBodyLabel("配置文件设置", self)
        self.descriptionLabel = CaptionLabel("如果没有配置文件，可以新建一个", self)

        self.iconLabel = IconWidget(FluentIcon.INFO, self)

        self.iconLabel.setFixedSize(24, 24)
        self.comboBox = EditableComboBox(self)
        self.loadButton = PushButton(FluentIcon.ROTATE, "加载配置", self)
        self.saveButton = PushButton(FluentIcon.SAVE, "存储配置", self)
        self.saveButton.setDisabled(True)

        self.cloudIcon = IconWidget(FluentIcon.CLOUD, self)
        self.cloudIcon.setFixedSize(24, 24)
        self.cloudBox = EditableComboBox(self)
        self.cloudRefreshButton = PushButton(FluentIcon.SYNC, "刷新云端列表", self)
        self.cloudImportButton = PushButton(FluentIcon.CLOUD_DOWNLOAD, "从云端导入", self)
        self.cloudUploadButton = PushButton(FluentIcon.UPDATE, "上传到云端", self)

        self.currProfileTitle = StrongBodyLabel("当前配置文件", self)
        self.currProfileContent = BodyLabel("", self)
        self.currProfileContent.setTextColor(QColor(0, 255, 0), QColor(255, 0, 0))

        self.vBoxLayout = QVBoxLayout(self)
        self.titleLayout = QHBoxLayout(self)
        self.title_separator = HorizontalSeparator(self)
        self.settingLayout = QHBoxLayout(self)
        self.cloudLayout = QHBoxLayout(self)
        self.currProfileLayout = QHBoxLayout(self)

        self.titleLayout.setContentsMargins(8, 8, 8, 0)  # (左, 上, 右, 下)
        self.titleLayout.addWidget(self.titleLabel, 1, Qt.AlignLeft)
        self.titleLayout.addWidget(self.descriptionLabel, 1, Qt.AlignRight)

        self.settingLayout.addSpacing(8)
        self.settingLayout.addWidget(self.iconLabel, 1)
        self.settingLayout.addSpacing(8)
        self.settingLayout.addWidget(self.comboBox, 3)
        self.settingLayout.addWidget(self.loadButton, 1)
        self.settingLayout.addWidget(self.saveButton, 1)

        self.cloudLayout.addSpacing(8)
        self.cloudLayout.addWidget(self.cloudIcon, 1)
        self.cloudLayout.addSpacing(8)
        self.cloudLayout.addWidget(self.cloudBox, 2)
        self.cloudLayout.addWidget(self.cloudRefreshButton, 1)
        self.cloudLayout.addWidget(self.cloudImportButton, 1)
        self.cloudLayout.addWidget(self.cloudUploadButton, 1)

        self.currProfileLayout.setContentsMargins(8, 8, 8, 0)  # (左, 上, 右, 下)
        self.currProfileLayout.addWidget(self.currProfileTitle, 1, Qt.AlignLeft)
        self.currProfileLayout.addWidget(self.currProfileContent, 1, Qt.AlignRight)

        self.vBoxLayout.addLayout(self.titleLayout)
        self.vBoxLayout.addWidget(self.title_separator)
        self.vBoxLayout.addLayout(self.settingLayout)
        self.vBoxLayout.addLayout(self.cloudLayout)
        self.vBoxLayout.addLayout(self.currProfileLayout)

        self.loadButton.clicked.connect(self.load_profile_local)
        self.saveButton.clicked.connect(self.save_profile_local)

        self.cloudRefreshButton.clicked.connect(self.refresh_profile_list_cloud)
        self.cloudImportButton.clicked.connect(self.load_profile_cloud)
        self.cloudUploadButton.clicked.connect(self.save_profile_cloud)

        self.refresh_profile_list_local()
        self.refresh_profile_list_cloud()

    def all_button_disable(self):
        self.saveButton.setDisabled(True)
        self.loadButton.setDisabled(True)
        self.cloudRefreshButton.setDisabled(True)
        self.cloudImportButton.setDisabled(True)
        self.cloudUploadButton.setDisabled(True)

    def all_button_enable(self):
        self.saveButton.setDisabled(False)
        self.loadButton.setDisabled(False)
        self.cloudRefreshButton.setDisabled(False)
        self.cloudImportButton.setDisabled(False)
        self.cloudUploadButton.setDisabled(False)

    def refresh_profile_list_cloud(self):
        self.all_button_disable()
        try:
            profiles = list_cloud_profile(path="profiles/")
            self.cloudBox.clear()
            self.cloudBox.setCurrentIndex(-1)
            for profile in profiles:
                self.cloudBox.addItem(profile)
        except Exception as e:
            self.show_error(str(e))
        self.all_button_enable()

    def refresh_profile_list_local(self):
        profiles = config.load_profile()
        self.comboBox.clear()
        self.comboBox.setCurrentIndex(-1)
        for k, v in profiles.items():
            self.comboBox.addItem(k)

    def show_error(self, error):
        w = Dialog("发生了一点小错误", error, self)
        w.yesButton.setText("我知道了")
        w.cancelButton.hide()
        w.buttonLayout.insertStretch(1)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')

    def show_msg(self, error):
        w = Dialog("提示", error, self)
        w.yesButton.setText("我知道了")
        w.cancelButton.hide()
        w.buttonLayout.insertStretch(1)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')

    def load_profile_cloud(self):
        self.all_button_disable()
        profile_name = self.cloudBox.currentText()
        if profile_name.strip() == "":
            return self.show_error("配置名文件未输入")
        try:
            profile = get_cloud_profile(profile_name, path="profiles/")
        except Exception as e:
            return self.show_error(str(e))
        self.show_msg("导入成功")
        return self.load_profile(profile, profile_name)

    def load_profile_local(self):
        self.all_button_disable()
        profile_name = self.comboBox.currentText()
        if profile_name.strip() == "":
            return self.show_error("配置名文件未输入")
        profile = config.load_profile(profile_name)
        if profile is None:
            return self.show_error("配置名异常")
        return self.load_profile(profile, profile_name)

    def load_profile(self, profile, profile_name):
        pprint.pprint(profile)
        window = self.window()
        load_ready = (window.rotationInterface.check_load_profile(profile) and
                      window.propertyInterface.check_load_profile(profile) and
                      window.macroInterface.check_load_profile(profile))
        if load_ready:
            window.rotationInterface.load_profile(profile)
            window.propertyInterface.load_profile(profile)
            window.macroInterface.load_profile(profile)
            self.currProfileContent.setText(profile_name)
            self.saveButton.setEnabled(True)
            window.profile_name = profile_name
            window.profile = profile
        else:
            w = Dialog("未加载", "所动信息都未发生变动", self)
            w.yesButton.setText("我知道了")
            w.cancelButton.hide()
            w.buttonLayout.insertStretch(1)
            if w.exec():
                print('Yes button is pressed')
            else:
                print('Cancel button is pressed')
        self.all_button_enable()

    def save_profile_cloud(self):
        self.all_button_disable()
        window = self.window()
        username = window.username

        profile = self.save_profile()
        profile_name = self.comboBox.currentText()
        profile_name = profile_name.split("@")[0]
        cloud_name = f"{profile_name}@{username}"
        self.cloudBox.setText(cloud_name)
        try:
            save_cloud_profile(cloud_name, profile, path="profiles/")
        except Exception as e:
            self.show_error("云存储失败")
        self.show_msg("上传成功")
        self.all_button_enable()

    def save_profile_local(self):
        self.all_button_disable()
        try:
            profile = self.save_profile()
            profile_name = self.comboBox.currentText()
        except Exception as e:
            self.show_error(str(e))
            self.all_button_enable()
            return
        config.save_profile(profile_name, profile)
        self.all_button_enable()

    def save_profile(self):
        window = self.window()

        profile = window.profile

        try:
            profile = window.rotationInterface.save_profile(profile)
            profile = window.propertyInterface.save_profile(profile)
            profile = window.macroInterface.save_profile(profile)
        except Exception as e:
            return self.show_error(str(e))
        if len(profile["rotation"]) < 100:
            return self.show_error("是不是搞错了啥？")

        return profile


class SettingInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.view = QWidget(self)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("SettingInterface")

        self.game_path_card = None
        self.rotation_profile_card = None
        self.activation_card = ActivationCard(self)
        self.appCard = AppInfoCard(self)

        self.vBoxLayout = QVBoxLayout(self.view)
        self.vBoxLayout.setSpacing(10)

        self.enableTransparentBackground()

        self.vBoxLayout.addWidget(self.appCard, 0, Qt.AlignTop)
        self.vBoxLayout.setSpacing(10)
        self.vBoxLayout.addWidget(self.activation_card, 0, Qt.AlignTop)
        self.vBoxLayout.addStretch(1)

        # self.act_app()

    def activate_software(self):
        self.activation_card.usernameEdit.setDisabled(True)
        self.activation_card.actCodeEdit.setDisabled(True)
        self.activation_card.machineCodeEdit.setDisabled(True)
        self.activation_card.actButton.setDisabled(True)
        self.vBoxLayout.removeWidget(self.activation_card)
        self.activation_card.deleteLater()

        self.game_path_card = GamePathCard(self)
        self.rotation_profile_card = RotationProfileCard(self)
        self.vBoxLayout.insertWidget(1, self.game_path_card, 0, Qt.AlignTop)
        self.vBoxLayout.insertWidget(2, self.rotation_profile_card, 0, Qt.AlignTop)

    def onActivated(self):
        pass
