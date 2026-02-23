# coding:utf-8
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QTextCursor
from PySide6.QtWidgets import (QHBoxLayout, QWidget, QVBoxLayout, QSizePolicy)
from qfluentwidgets import (BodyLabel, TitleLabel,
                            ScrollArea, PushButton, TextEdit)

from app.common import config
from app.common.utils import generate_count_dict, split_list, extract_prop_arguments, check_lua_code, \
    parse_key_arguments
from app.generator.battle_ogic import battle_logic_generator
from app.generator.final_file import final_file_generator
from app.generator.macro_dict import macro_dict_generator
from app.generator.macro_keybindings import macro_keybindings_generator
from app.generator.prop_func import prop_func_generator
from app.generator.public_func import public_func_generator


class AddonGeneratorThread(QThread):
    # 定义信号以更新主窗口
    logging = Signal(str)
    finished_signal = Signal(bool)

    def __init__(self, profile_name: str, profile: dict, game_path: Path):
        super().__init__()
        self.profile_name = profile_name
        self.profile = profile
        self.game_path = game_path

        self.addons_dir = self.game_path.joinpath("Interface").joinpath("AddOns").joinpath("PixelRotationLT")
        if not self.addons_dir.exists():
            self.addons_dir.mkdir()

    def get_props_from_profile(self, profile):
        self.logging.emit("===========读取Props============")
        rotation_text = profile.get("rotation", None)
        if rotation_text is None:
            self.logging.emit(f"{self.profile_name}缺少rotation")
            raise ValueError(f"{self.profile_name}缺少rotation")
        # rotation_props = generate_count_dict(extract_prop_arguments(rotation_text, "Prop"))
        # pprint.pprint(rotation_props)
        rotation_props2 = parse_key_arguments(rotation_text, "Prop")
        # pprint.pprint(rotation_props2)
        props_list = []
        for prop in rotation_props2:
            props_list.append(prop["title"])
        self.logging.emit(f"rotation有总计{len(props_list)}个Props，清单是：")
        for sub_list in split_list(props_list, 5):
            self.logging.emit(" , ".join(sub_list))

        if len(props_list) == 0:
            self.logging.emit(f"Props数量为0！！！")
            raise ValueError(f"Props数量为0！！！")
        return props_list

    def get_macros_from_profile(self, profile):
        self.logging.emit("===========读取Cast============")
        rotation_text = profile.get("rotation", None)
        if rotation_text is None:
            self.logging.emit(f"{self.profile_name}缺少rotation")
            raise ValueError(f"{self.profile_name}缺少rotation")
        rotation_macros = generate_count_dict(extract_prop_arguments(rotation_text, "Cast"))
        macro_list = []
        for macro in rotation_macros:
            macro_list.append(macro["string"])
        self.logging.emit(f"rotation有总计{len(macro_list)}个Cast，清单是：")
        for sub_list in split_list(macro_list, 5):
            self.logging.emit(" , ".join(sub_list))

        if len(macro_list) == 0:
            self.logging.emit(f"Cast数量为0！！！")
            raise ValueError(f"Cast数量为0！！！")
        return macro_list

    def check_props(self, rotation_props, profile):
        self.logging.emit("===========检查Prop============")
        has_error = False
        result = []
        func_list = []
        self.logging.emit(f"开始逐个检查Prop")
        profile_props = profile.get("properties", {})
        for prop_title in rotation_props:
            prop = profile_props.get(prop_title, None)
            if prop is None:
                self.logging.emit(f"{prop_title}在配置项中不存在")
                has_error = True
                continue

            code = prop.get("code", "")
            func_args = prop.get("func_args", [])
            func_name = prop.get("func_name", "")
            code_string = f"local function {func_name}(" + ", ".join(func_args) + ")\n"  # 生成函数调用字符串
            code_string += code
            code_string += "\nend"
            print(code_string)

            lua_error = check_lua_code(code_string)
            if len(prop["code"]) < 10:
                self.logging.emit(f"{prop_title}的代码太短了")
                has_error = True
            if lua_error.strip() == "":
                self.logging.emit(f"代码正常：\"{prop_title}\"")
            else:
                self.logging.emit(f"代码有错误：\"{prop_title}\"，错误是：{lua_error}")
                has_error = True
            func_name = prop.get("func_name", "")
            if func_name == '':
                self.logging.emit(f"{prop_title}的变量名没有设置")
                has_error = True
            if func_name in func_list:
                self.logging.emit(f"{prop_title}的变量名重复")
                has_error = True
            func_list.append(func_name)
            prop["title"] = prop_title
            result.append(prop)
        self.logging.emit(f"Props检查完毕，总计{len(result)}个Props")
        if has_error:
            raise ValueError(f"check_props包含错误")
        else:
            return result

    def check_code(self, code, title):
        lua_error = check_lua_code(code)
        if lua_error.strip() == "":
            self.logging.emit(f"{title}校验成功")
        else:
            self.logging.emit(f"{title}校验失败，错误是：{lua_error}")
            raise ValueError(f"{title}校验失败，错误是：{lua_error}")

    def check_macros(self, rotation_macros, profile):
        self.logging.emit("===========检查Marcos============")
        result = []
        has_error = False
        color_list = []
        key_list = []
        self.logging.emit(f"开始逐个检查Macro")
        profile_macros = profile.get("macros", {})
        for macro_title in rotation_macros:
            macro = profile_macros.get(macro_title, None)
            if macro is None:
                self.logging.emit(f"{macro_title}在配置项中不存在")
                has_error = True
                continue
            if len(macro["code"].strip()) < 5:
                self.logging.emit(f"{macro_title}的代码太短了")
                has_error = True
                continue
            key = macro.get("key", "")
            color = macro.get("color", "")
            if (key == "") or (color == ''):
                self.logging.emit(f"{macro_title}的颜色或快捷键没有设置")
                has_error = True
                continue
            if (key in key_list) or (color in color_list):
                self.logging.emit(f"{macro_title}的颜色或快捷键重复")
                has_error = True
                continue
            color_list.append(color)
            key_list.append(key)
            macro["title"] = macro_title
            result.append(macro)
            self.logging.emit(f"Macro:\"{macro_title}\"检查正常")

        if has_error:
            raise ValueError("check_macros代码检测失败")
        else:
            return result

    def run(self):
        profile = self.profile

        rotation_properties = self.get_props_from_profile(profile)
        # pprint.pprint(rotation_properties)
        used_props = self.check_props(rotation_properties, profile)
        # pprint.pprint(used_props)

        rotation_macros = self.get_macros_from_profile(profile)
        used_macros = self.check_macros(rotation_macros, profile)

        key_bind_lua = macro_keybindings_generator(used_macros)
        self.check_code(key_bind_lua, "键位绑定代码")

        macro_dict_lua = macro_dict_generator(used_macros)
        self.check_code(macro_dict_lua, "宏字典代码")

        # pprint.pprint(used_props)
        prop_func_lua = prop_func_generator(used_props)
        self.check_code(prop_func_lua, "参数逻辑代码")

        battle_logic_lua = battle_logic_generator(profile, used_props, used_macros)
        # print(battle_logic_lua)
        self.check_code(battle_logic_lua, "战斗逻辑代码")

        public_func_lua = public_func_generator(interrupt_spell_list=config.load_value("interrupt_spell_list", []),
                                                interrupt_black_list=config.load_value("interrupt_black_list", []),
                                                important_spell_list=config.load_value("important_spell_list", []), )

        final_lua, toc_code = final_file_generator(key_bind_lua,public_func_lua, macro_dict_lua, prop_func_lua, battle_logic_lua)
        open(self.addons_dir.joinpath("PixelRotationLT.lua"), "w", encoding="utf-8").write(final_lua)
        open(self.addons_dir.joinpath("PixelRotationLT.toc"), "w", encoding="utf-8").write(toc_code)
        self.check_code(final_lua, "最终文件代码")

        self.finished_signal.emit(True)
        return True


class GenerateInterface(ScrollArea):
    def __init__(self, parent=None):
        """
        初始化BotInterface类的实例。

        :param parent: 父窗口，默认为None
        """
        super().__init__(parent=parent)

        # 创建一个QWidget作为主视图
        self.view = QWidget(self)
        # 设置主视图为可调整大小
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        # 设置对象名称为BotInterface
        self.setObjectName("GenerateInterface")

        # 创建一个BodyLabel用于显示当前设置的标签
        self.currentProfileLabel = BodyLabel("当前设置", self.view)
        # 创建一个TitleLabel用于显示当前配置的编辑框
        self.currentProfileEdit = TitleLabel("还未加载配置", self.view)

        # 创建一个PushButton用于生成插件
        self.generateAddonButton = PushButton("生成插件", self.view)
        # 连接按钮的点击事件到start_addon_generation方法
        self.generateAddonButton.clicked.connect(self.start_addon_generation)
        # 创建一个PushButton用于运行脚本
        # self.runBotButton = PushButton("运行脚本", self.view)

        # 禁用运行脚本按钮
        # self.runBotButton.setDisabled(True)
        # 禁用生成插件按钮
        self.generateAddonButton.setDisabled(True)

        # 创建一个TextEdit用于显示日志
        self.log_text_edit = TextEdit(self.view)
        # 设置日志编辑框为只读
        self.log_text_edit.setReadOnly(True)
        # 设置日志编辑框的大小策略为可扩展
        self.log_text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        # 设置日志编辑框的固定高度为750像素
        self.log_text_edit.setFixedHeight(750)

        # 创建一个垂直布局管理器
        self.vBoxLayout = QVBoxLayout(self.view)
        # 设置布局管理器的间距为10像素
        self.vBoxLayout.setSpacing(10)

        # 创建一个垂直布局管理器用于当前配置
        self.currentProfileLayout = QVBoxLayout(self.view)
        # 将当前配置标签添加到布局中
        self.currentProfileLayout.addWidget(self.currentProfileLabel)
        # 将当前配置编辑框添加到布局中
        self.currentProfileLayout.addWidget(self.currentProfileEdit)

        # 创建一个水平布局管理器用于按钮
        self.buttonLayout = QHBoxLayout(self.view)
        # 将生成插件按钮添加到布局中
        self.buttonLayout.addWidget(self.generateAddonButton)
        # 将运行脚本按钮添加到布局中
        # self.buttonLayout.addWidget(self.runBotButton)

        # 创建一个水平布局管理器用于第一层
        self.L1Layout = QHBoxLayout(self.view)
        # 将当前配置布局添加到第一层布局中
        self.L1Layout.addLayout(self.currentProfileLayout)
        # 将按钮布局添加到第一层布局中
        self.L1Layout.addLayout(self.buttonLayout)

        # 创建一个水平布局管理器用于第五层
        self.L5Layout = QHBoxLayout(self.view)
        # 将日志编辑框添加到第五层布局中
        self.L5Layout.addWidget(self.log_text_edit)

        # 将第一层布局添加到垂直布局管理器中
        self.vBoxLayout.addLayout(self.L1Layout)
        # 将第五层布局添加到垂直布局管理器中
        self.vBoxLayout.addLayout(self.L5Layout)
        # 在垂直布局管理器中添加一个可伸缩的空白项
        self.vBoxLayout.addStretch(1)

        # 启用透明背景
        self.enableTransparentBackground()

        # 初始化线程为None
        self.thread = None

    def onActivated(self):
        window = self.window()
        if window.profile_name is not None:
            self.currentProfileEdit.setText(window.profile_name)
            # self.runBotButton.setEnabled(True)
            self.generateAddonButton.setEnabled(True)

    @staticmethod
    def get_current_time():
        """获取当前时间（小时:分钟:秒.毫秒）"""
        now = datetime.now()
        return now.strftime("%H:%M:%S.%f")[:-3]  # 只保留毫秒部分

    def add_log(self, text):
        """添加日志信息，格式为 '时:分:秒.毫秒 - 日志内容'"""
        current_time = self.get_current_time()
        log_message = f"{current_time} - {text}"
        self.log_text_edit.append(log_message)  # 在文本编辑器中添加日志

        cursor = self.log_text_edit.textCursor()  # 获取光标
        cursor.movePosition(QTextCursor.End)  # 将光标移动到文本末尾
        self.log_text_edit.setTextCursor(cursor)

    def start_addon_generation(self):
        window = self.window()
        game_path = config.load_value("GamePath")

        if not Path(game_path).exists():
            return self.add_log("游戏路径不存在")

        addons_dir = Path(game_path).joinpath("Interface").joinpath("AddOns").joinpath("PixelRotationLT")
        addons_dir.mkdir(exist_ok=True, parents=True)
        if not addons_dir.exists():
            return self.add_log("插件目录不存在")

        # 创建插件生成线程，并传递必要的数据
        self.thread = AddonGeneratorThread(profile_name=window.profile_name, profile=window.profile,
                                           game_path=Path(game_path))
        self.thread.logging.connect(self.add_log)
        self.thread.finished_signal.connect(self.on_generation_finished)
        self.thread.start()

        # self.runBotButton.setDisabled(True)
        self.generateAddonButton.setDisabled(True)

    def on_generation_finished(self, result):
        # self.runBotButton.setEnabled(True)
        self.generateAddonButton.setEnabled(True)
