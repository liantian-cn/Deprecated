import re
import os
import sys
import json
import time
import uuid
import base64
import ctypes
import random
import string
import hashlib
import platform
import win32gui
import importlib
from pathlib import Path
from datetime import datetime

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from PIL import ImageGrab
from PySide6.QtCore import QThread, Signal, Qt, QByteArray
from PySide6.QtGui import QIcon, QPixmap, QTextCursor
from PySide6.QtWidgets import QApplication, QFrame, QHBoxLayout, QVBoxLayout, QWidget, QFileDialog, QSizePolicy
from qfluentwidgets import (Dialog, FluentIcon, IconWidget, BodyLabel, PushButton, SimpleCardWidget, PlainTextEdit,
                            SubtitleLabel, HeaderCardWidget, PrimaryPushButton, setFont, ScrollArea, MSFluentWindow,
                            ComboBox, TextEdit, StrongBodyLabel, LineEdit)
from resource.logo2 import image_data as logo_data_base64

DEV_MODE = True
if DEV_MODE:
    BASE_DIR = Path(os.path.dirname(os.path.abspath(__file__)))
else:
    BASE_DIR = Path(os.path.dirname(sys.argv[0]))
# print(BASE_DIR)
SALT_LENGTH = 8
SALT_CHARS = string.ascii_letters + string.digits
AES_KEY = b'&\tw\x8a\xdd\xe1@\x80\x8af\xd7\x07\xd3\x98\x93\x93W\xc8N\xf7\x10\xe3\x89=\xeb\xb2\xbcg\xf4\x7f(\xb6'

CONFIG_FILE = BASE_DIR.joinpath("licence.key")

WM_KEYDOWN = 0x0100
WM_KEYUP = 0x0101

VK_DICT = {
    "NUMPAD0": 0x60,
    "NUMPAD1": 0x61,
    "NUMPAD2": 0x62,
    "NUMPAD3": 0x63,
    "NUMPAD4": 0x64,
    "NUMPAD5": 0x65,
    "NUMPAD6": 0x66,
    "NUMPAD7": 0x67,
    "NUMPAD8": 0x68,
    "NUMPAD9": 0x69,
    "SHIFT": 0x10,
    "CTRL": 0x11,
    "ALT": 0x12,
    "F1": 0x70,
    "F2": 0x71,
    "F3": 0x72,
    "F4": 0x73,
    "F5": 0x74,
    "F6": 0x75,
    "F7": 0x76,
    "F8": 0x77,
    "F9": 0x78,
    "F10": 0x79,
    "F11": 0x7a,
    "F12": 0x7b,
}

KEY_COLOR_MAP = [
    {'keybind': 'SHIFT-F2', 'r': 0, 'g': 255, 'b': 128, },
    {'keybind': 'SHIFT-F3', 'r': 0, 'g': 255, 'b': 140, },
    {'keybind': 'SHIFT-F5', 'r': 0, 'g': 255, 'b': 153, },
    {'keybind': 'SHIFT-F6', 'r': 0, 'g': 255, 'b': 166, },
    {'keybind': 'SHIFT-F7', 'r': 0, 'g': 255, 'b': 179, },
    {'keybind': 'SHIFT-F8', 'r': 0, 'g': 255, 'b': 191, },
    {'keybind': 'SHIFT-F9', 'r': 0, 'g': 255, 'b': 204, },
    {'keybind': 'SHIFT-F10', 'r': 0, 'g': 255, 'b': 217, },
    {'keybind': 'SHIFT-F11', 'r': 0, 'g': 255, 'b': 229, },
    {'keybind': 'SHIFT-F12', 'r': 0, 'g': 255, 'b': 242, },
    {'keybind': 'CTRL-F2', 'r': 128, 'g': 255, 'b': 0, },
    {'keybind': 'CTRL-F3', 'r': 115, 'g': 255, 'b': 0, },
    {'keybind': 'CTRL-F5', 'r': 102, 'g': 255, 'b': 0, },
    {'keybind': 'CTRL-F6', 'r': 89, 'g': 255, 'b': 0, },
    {'keybind': 'CTRL-F7', 'r': 77, 'g': 255, 'b': 0, },
    {'keybind': 'CTRL-F8', 'r': 64, 'g': 255, 'b': 0, },
    {'keybind': 'CTRL-F9', 'r': 51, 'g': 255, 'b': 0, },
    {'keybind': 'CTRL-F10', 'r': 38, 'g': 255, 'b': 0, },
    {'keybind': 'CTRL-F11', 'r': 26, 'g': 255, 'b': 0, },
    {'keybind': 'CTRL-F12', 'r': 13, 'g': 255, 'b': 0, },
    {'keybind': 'CTRL-SHIFT-F2', 'r': 0, 'g': 0, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-F3', 'r': 13, 'g': 0, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-F5', 'r': 25, 'g': 0, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-F6', 'r': 38, 'g': 0, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-F7', 'r': 51, 'g': 0, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-F8', 'r': 64, 'g': 0, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-F9', 'r': 76, 'g': 0, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-F10', 'r': 89, 'g': 0, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-F11', 'r': 102, 'g': 0, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-F12', 'r': 115, 'g': 0, 'b': 255, },
    {'keybind': 'CTRL-NUMPAD1', 'r': 255, 'g': 0, 'b': 0, },
    {'keybind': 'CTRL-NUMPAD2', 'r': 255, 'g': 13, 'b': 0, },
    {'keybind': 'CTRL-NUMPAD3', 'r': 255, 'g': 25, 'b': 0, },
    {'keybind': 'CTRL-NUMPAD4', 'r': 255, 'g': 38, 'b': 0, },
    {'keybind': 'CTRL-NUMPAD5', 'r': 255, 'g': 51, 'b': 0, },
    {'keybind': 'CTRL-NUMPAD6', 'r': 255, 'g': 64, 'b': 0, },
    {'keybind': 'CTRL-NUMPAD7', 'r': 255, 'g': 77, 'b': 0, },
    {'keybind': 'CTRL-NUMPAD8', 'r': 255, 'g': 89, 'b': 0, },
    {'keybind': 'CTRL-NUMPAD9', 'r': 255, 'g': 102, 'b': 0, },
    {'keybind': 'CTRL-NUMPAD0', 'r': 255, 'g': 115, 'b': 0, },
    {'keybind': 'SHIFT-NUMPAD1', 'r': 255, 'g': 255, 'b': 0, },
    {'keybind': 'SHIFT-NUMPAD2', 'r': 242, 'g': 255, 'b': 0, },
    {'keybind': 'SHIFT-NUMPAD3', 'r': 230, 'g': 255, 'b': 0, },
    {'keybind': 'SHIFT-NUMPAD4', 'r': 217, 'g': 255, 'b': 0, },
    {'keybind': 'SHIFT-NUMPAD5', 'r': 204, 'g': 255, 'b': 0, },
    {'keybind': 'SHIFT-NUMPAD6', 'r': 191, 'g': 255, 'b': 0, },
    {'keybind': 'SHIFT-NUMPAD7', 'r': 178, 'g': 255, 'b': 0, },
    {'keybind': 'SHIFT-NUMPAD8', 'r': 166, 'g': 255, 'b': 0, },
    {'keybind': 'SHIFT-NUMPAD9', 'r': 153, 'g': 255, 'b': 0, },
    {'keybind': 'SHIFT-NUMPAD0', 'r': 140, 'g': 255, 'b': 0, },
    {'keybind': 'CTRL-SHIFT-NUMPAD1', 'r': 0, 'g': 255, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-NUMPAD2', 'r': 0, 'g': 242, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-NUMPAD3', 'r': 0, 'g': 229, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-NUMPAD4', 'r': 0, 'g': 217, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-NUMPAD5', 'r': 0, 'g': 204, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-NUMPAD6', 'r': 0, 'g': 191, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-NUMPAD7', 'r': 0, 'g': 178, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-NUMPAD8', 'r': 0, 'g': 166, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-NUMPAD9', 'r': 0, 'g': 153, 'b': 255, },
    {'keybind': 'CTRL-SHIFT-NUMPAD0', 'r': 0, 'g': 140, 'b': 255, },
    {'keybind': 'ALT-NUMPAD1', 'r': 255, 'g': 128, 'b': 0, },
    {'keybind': 'ALT-NUMPAD2', 'r': 255, 'g': 140, 'b': 0, },
    {'keybind': 'ALT-NUMPAD3', 'r': 255, 'g': 153, 'b': 0, },
    {'keybind': 'ALT-NUMPAD4', 'r': 255, 'g': 166, 'b': 0, },
    {'keybind': 'ALT-NUMPAD5', 'r': 255, 'g': 178, 'b': 0, },
    {'keybind': 'ALT-NUMPAD6', 'r': 255, 'g': 191, 'b': 0, },
    {'keybind': 'ALT-NUMPAD7', 'r': 255, 'g': 204, 'b': 0, },
    {'keybind': 'ALT-NUMPAD8', 'r': 255, 'g': 217, 'b': 0, },
    {'keybind': 'ALT-NUMPAD9', 'r': 255, 'g': 229, 'b': 0, },
    {'keybind': 'ALT-NUMPAD0', 'r': 255, 'g': 242, 'b': 0, },
    {'keybind': 'ALT-SHIFT-NUMPAD1', 'r': 0, 'g': 128, 'b': 255, },
    {'keybind': 'ALT-SHIFT-NUMPAD2', 'r': 0, 'g': 115, 'b': 255, },
    {'keybind': 'ALT-SHIFT-NUMPAD3', 'r': 0, 'g': 102, 'b': 255, },
    {'keybind': 'ALT-SHIFT-NUMPAD4', 'r': 0, 'g': 89, 'b': 255, },
    {'keybind': 'ALT-SHIFT-NUMPAD5', 'r': 0, 'g': 76, 'b': 255, },
    {'keybind': 'ALT-SHIFT-NUMPAD6', 'r': 0, 'g': 64, 'b': 255, },
    {'keybind': 'ALT-SHIFT-NUMPAD7', 'r': 0, 'g': 51, 'b': 255, },
    {'keybind': 'ALT-SHIFT-NUMPAD8', 'r': 0, 'g': 38, 'b': 255, },
    {'keybind': 'ALT-SHIFT-NUMPAD9', 'r': 0, 'g': 25, 'b': 255, },
    {'keybind': 'ALT-SHIFT-NUMPAD0', 'r': 0, 'g': 13, 'b': 255, },
    {'keybind': 'ALT-SHIFT-F2', 'r': 128, 'g': 0, 'b': 255, },
    {'keybind': 'ALT-SHIFT-F3', 'r': 140, 'g': 0, 'b': 255, },
    {'keybind': 'ALT-SHIFT-F5', 'r': 153, 'g': 0, 'b': 255, },
    {'keybind': 'ALT-SHIFT-F6', 'r': 166, 'g': 0, 'b': 255, },
    {'keybind': 'ALT-SHIFT-F7', 'r': 179, 'g': 0, 'b': 255, },
    {'keybind': 'ALT-SHIFT-F8', 'r': 191, 'g': 0, 'b': 255, },
    {'keybind': 'ALT-SHIFT-F9', 'r': 204, 'g': 0, 'b': 255, },
    {'keybind': 'ALT-SHIFT-F10', 'r': 217, 'g': 0, 'b': 255, },
    {'keybind': 'ALT-SHIFT-F11', 'r': 230, 'g': 0, 'b': 255, },
    {'keybind': 'ALT-SHIFT-F12', 'r': 242, 'g': 0, 'b': 255, },
    {'keybind': 'ALT-F2', 'r': 0, 'g': 255, 'b': 0, },
    {'keybind': 'ALT-F3', 'r': 0, 'g': 255, 'b': 13, },
    {'keybind': 'ALT-F5', 'r': 0, 'g': 255, 'b': 25, },
    {'keybind': 'ALT-F6', 'r': 0, 'g': 255, 'b': 38, },
    {'keybind': 'ALT-F7', 'r': 0, 'g': 255, 'b': 51, },
    {'keybind': 'ALT-F8', 'r': 0, 'g': 255, 'b': 64, },
    {'keybind': 'ALT-F9', 'r': 0, 'g': 255, 'b': 77, },
    {'keybind': 'ALT-F10', 'r': 0, 'g': 255, 'b': 89, },
    {'keybind': 'ALT-F11', 'r': 0, 'g': 255, 'b': 102, },
]

MOD_MAP = {
    "CTRL": 0x0002,  # MOD_CONTROL
    "CONTROL": 0x0002,
    "SHIFT": 0x0004,  # MOD_SHIFT
    "ALT": 0x0001,  # MOD_ALT
}
user32 = ctypes.WinDLL('user32', use_last_error=True)


def parse_hotkey(keybind_str):
    """
    解析快捷键字符串为（修饰符组合值, 虚拟键码）
    示例：'CTRL-SHIFT-F12' -> (0x0002|0x0004, 0x7b)
    """
    parts = keybind_str.upper().split('-')
    modifiers = 0
    vk_code = None

    for part in parts:
        if part in MOD_MAP:
            modifiers |= MOD_MAP[part]
        elif part in VK_DICT:
            vk_code = VK_DICT[part]
        else:
            raise ValueError(f"无效的键位标识: {part} in {keybind_str}")

    if vk_code is None:
        raise ValueError(f"未找到主键: {keybind_str}")

    return modifiers, vk_code


def check_hotkey_conflicts(key_list):
    """
    检查并过滤被占用的快捷键
    返回：过滤后的key_list（仅包含可用快捷键）
    """
    valid_keys = []

    for idx, item in enumerate(key_list, start=1):
        keybind = item['keybind']
        try:
            mod, vk = parse_hotkey(keybind)
            # 尝试注册热键（使用唯一递增ID）
            if user32.RegisterHotKey(None, idx, mod, vk):
                user32.UnregisterHotKey(None, idx)  # 立即释放
                valid_keys.append(item)  # 添加可用项
            else:
                # 获取错误信息（可选记录日志）
                error_code = ctypes.get_last_error()
        except Exception as e:
            # 非法快捷键配置（自动过滤）
            pass

    return valid_keys


KEY_COLOR_MAP = check_hotkey_conflicts(KEY_COLOR_MAP)


def gen_macros_text(macro_list: list) -> str:
    template_string = "ShionSpellMacro[\"$macro_name\"] = { $macro_r, $macro_g, $macro_b, \"$macro_text\", \"$macro_keybind\" }"
    macros_text = ""
    for macro in macro_list:
        x = template_string.replace("$macro_name", macro["macro_name"])
        x = x.replace("$macro_r", str(macro["macro_r"]))
        x = x.replace("$macro_g", str(macro["macro_g"]))
        x = x.replace("$macro_b", str(macro["macro_b"]))
        x = x.replace("$macro_text", "\\n".join(
            macro["macro_text"].split("\n")))
        x = x.replace("$macro_keybind", str(macro["macro_keybind"]))
        macros_text += x + "\n"
    return macros_text


def gen_spell_text(code_list) -> str:
    result = ""
    for a in code_list:
        code = a["code"]
        spell_list = load_value(code, [])
        if spell_list is not None:
            spell_list = [str(spell) for spell in spell_list]
            for spell in spell_list:
                result += f"{code}[{spell}] = true;\n"
    return result


def get_random_string(length: int = 32, chars: str = SALT_CHARS) -> str:
    return ''.join(random.choice(chars) for i in range(length))


def extract_prop_arguments(text, key):
    # 正则表达式用于匹配 Prop 函数调用的参数
    pattern = rf'{key}\s*\(\s*"([^"]*?)"\s*\)'
    # pattern = rf'{key}\s*\(\s*((?:[^)]|\))*)\)'

    # 使用 re.findall() 找到所有匹配的参数
    matches = re.findall(pattern, text)

    return matches


def prepare_the_str(key: str) -> str:
    # 如果key不是block_size的整数倍，则补齐
    while len(key) % AES.block_size != 0:
        key += '\0'
    return key


def prepare_the_bytes(key: bytes) -> bytes:
    # 如果key不是block_size的整数倍，则补齐
    while len(key) % AES.block_size != 0:
        key += b'\0'
    return key


def prepare_b64_decode(encrypted_str: str) -> str:
    # 为base64解密的字符串补齐=
    missing_padding = 4 - len(encrypted_str) % 4
    if missing_padding:
        encrypted_str += '=' * missing_padding
    return encrypted_str


def bytes_encrypt(plain_bytes: bytes) -> bytes:
    nonce = get_random_bytes(12)
    cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=nonce)
    return cipher.encrypt(plain_bytes) + nonce


def bytes_decrypt(encrypted_bytes: bytes) -> bytes:
    nonce = encrypted_bytes[-12:]
    encrypted_bytes = encrypted_bytes[:-12]
    cipher = AES.new(AES_KEY, AES.MODE_GCM, nonce=nonce)
    return cipher.decrypt(encrypted_bytes)


def string_encrypt(plain_str: str) -> str:
    # 先将文字补足长度，转换为bytes
    plain_str = prepare_the_str(plain_str)
    plain_bytes = plain_str.encode()
    encrypted_bytes = bytes_encrypt(plain_bytes)
    encrypted_b64 = base64.urlsafe_b64encode(encrypted_bytes)
    encrypted_str = str(
        encrypted_b64, encoding='utf-8').strip().replace('=', '')
    return encrypted_str


def string_decrypt(encrypted_str: str) -> str:
    encrypted_str = prepare_b64_decode(encrypted_str)
    encrypted_bytes = base64.urlsafe_b64decode(
        encrypted_str.encode(encoding='utf-8'))
    plain_bytes = bytes_decrypt(encrypted_bytes)
    plain_str = str(plain_bytes, encoding='utf-8').replace('\0', '')
    return plain_str


def encrypt2file_s(plain: str, file_path: Path) -> int:
    header = b'u:'
    plain_b = plain.encode('utf-8')
    return file_path.write_bytes(header + bytes_encrypt(plain_b))


def decrypt2file_s(file_path: Path) -> str:
    file_bytes = file_path.read_bytes()
    encrypted_bytes = file_bytes[len(b'u:'):]
    plain_bytes = bytes_decrypt(encrypted_bytes)
    return plain_bytes.decode('utf-8')


def encrypt2file_b(plain: bytes, file_path: Path) -> int:
    header = b'b:'
    return file_path.write_bytes(header + bytes_encrypt(plain))


def decrypt2file_b(file_path: Path) -> bytes:
    file_bytes = file_path.read_bytes()
    encrypted_bytes = file_bytes[len(b'b:'):]
    plain_bytes = bytes_decrypt(encrypted_bytes)
    return plain_bytes


def obj2file(obj, file_path: Path) -> int:
    return encrypt2file_s(json.dumps(obj), file_path)


def file2obj(file_path: Path):
    return json.loads(decrypt2file_s(file_path))


def init_config():
    cfg = {
        "profiles": "",
        "GamePath": "X:/World of Warcraft/_retail_",
    }
    if not CONFIG_FILE.exists():
        obj2file(cfg, CONFIG_FILE)


def load_value(key, default=None):
    cfg = file2obj(CONFIG_FILE)
    return cfg.get(key, default)  # 如果key不存在，返回None


def save_key_value(key, value):
    cfg = file2obj(CONFIG_FILE)
    cfg[key] = value
    obj2file(cfg, CONFIG_FILE)


def generate_unique_strings(num_strings, length=24):
    if num_strings > 1000:
        raise ValueError("数量不能超过1000个字符串。")

    unique_strings = set()  # 使用集合以确保唯一性

    while len(unique_strings) < num_strings:
        # 生成一个由大小写字母组成的字符串
        random_string = ''.join(random.choices(string.ascii_letters, k=length))
        unique_strings.add(random_string)  # 将字符串添加到集合中

    return list(unique_strings)  # 返回字符串列表


def get_windows_by_title(title):
    windows = []
    win32gui.EnumWindows(lambda hwnd, _: windows.append(
        (hwnd, win32gui.GetWindowText(hwnd))), None)
    return [hwnd for hwnd, window_title in windows if title.lower() in window_title.lower()]


def press_key_hwnd(hwnd, skey):
    key = VK_DICT.get(skey)
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYDOWN, key, 0)


def release_key_hwnd(hwnd, skey):
    key = VK_DICT.get(skey)
    ctypes.windll.user32.PostMessageW(hwnd, WM_KEYUP, key, 0)


def press_and_release_key_hwnd(hwnd, skey):
    press_key_hwnd(hwnd, skey)
    time.sleep(0.05)
    release_key_hwnd(hwnd, skey)


print(DEV_MODE)
if DEV_MODE:
    from LuaCore import lua_01_header, lua_04_footer, toc_content

    lua_rtk = BASE_DIR.joinpath(f"lua.lkf")
    if lua_rtk.exists():
        lua_rtk.unlink()
    obj2file({"header": lua_01_header,
              "footer": lua_04_footer,
              "toc_content": toc_content}, lua_rtk)
else:
    lua_rtk = BASE_DIR.joinpath(f"lua.lkf")
    obj = file2obj(lua_rtk)
    lua_01_header = obj.get("header")
    lua_04_footer = obj.get("footer")
    toc_content = obj.get("toc_content")


def get_machine_code():
    # 获取系统的唯一标识符
    machine_uuid = str(uuid.getnode())

    # 获取系统信息
    system_info = platform.uname()
    system_details = f"{system_info.system}-{system_info.node}-{system_info.release}-{system_info.version}-{system_info.machine}"

    # 组合信息
    combined_info = machine_uuid + system_details
    machine_code = combined_info

    for _ in range(1072):
        machine_code = hashlib.sha256(machine_code.encode()).hexdigest()

    return machine_code


def get_act_code():
    machine_code = get_machine_code()
    return machine_code


class Keyboard:
    def __init__(self):
        self.hwnd = None

    def find_window(self, title):
        windows = get_windows_by_title(title)
        if windows:
            self.hwnd = windows[0]
            return True
        else:
            return False

    def send_hot_key(self, hot_key):
        key_list = hot_key.split("-")
        for skey in key_list:
            press_key_hwnd(self.hwnd, skey)
        time.sleep(0.01)
        for skey in key_list:
            release_key_hwnd(self.hwnd, skey)


class BotWorker(QThread):
    stop_signal = Signal()
    output_signal = Signal(dict)

    def __init__(self):
        super().__init__()
        self.color_to_key = {}
        for x in KEY_COLOR_MAP:
            self.color_to_key[(x["r"], x["g"], x["b"])] = x["keybind"]

        self.monitor = {"top": 0, "left": 0, "width": 16, "height": 16}
        self.stop_signal.connect(self.handle_stop)
        self.keyboard = None
        self.is_running = False

    @staticmethod
    def capture_screen_region(
            left: int = 0,
            top: int = 0,
            width: int = 16,
            height: int = 16
    ) -> ImageGrab.Image:
        bbox = (left, top, left + width, top + height)
        return ImageGrab.grab(bbox=bbox)

    def setup(self):
        self.keyboard = Keyboard()
        if not self.keyboard.find_window("魔兽世界"):
            self.output_signal.emit({"error": f"未找到魔兽世界窗口"})
            raise ValueError("未找到魔兽世界窗口")

    def run(self):
        self.is_running = True
        self.keyboard.send_hot_key("ALT-F12")
        while self.is_running:
            time.sleep(random.uniform(0.25, 0.3))
            img = self.capture_screen_region()
            if img is None:
                self.output_signal.emit({"error": f"未捕获到图像"})
                continue
            # img = self.camera.screenshot(region=self.region)
            pixels = list(img.getdata())
            unique_colors = set(pixels)
            if len(unique_colors) != 1:
                self.output_signal.emit(
                    {"error": f"颜色复杂度：{len(unique_colors)}"})
            else:
                pixel_color = pixels[0]

                key_bind = self.color_to_key.get(pixel_color, None)
                if key_bind is not None:
                    self.keyboard.send_hot_key(key_bind)
                    self.output_signal.emit(
                        {"key_bind": key_bind, "color": str(pixel_color)})
                else:
                    self.output_signal.emit({
                        "error": f"未找到颜色：{str(pixel_color)}"
                    })

        self.output_signal.emit({"error": f"捕获已完全停止"})

    def handle_stop(self):
        self.is_running = False


class Widget(QFrame):

    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        self.label = SubtitleLabel(text, self)
        self.hBoxLayout = QHBoxLayout(self)

        setFont(self.label, 24)
        self.label.setAlignment(Qt.AlignCenter)
        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        self.setObjectName(text.replace(' ', '-'))


class SettingInterface(ScrollArea):
    class ActivationCard(HeaderCardWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setTitle('软件激活')
            self.setBorderRadius(8)
            self.vBoxLayout = QVBoxLayout()
            self.vBoxLayout.setSpacing(16)
            self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

            self.machineCodeLabel = StrongBodyLabel("机器码:", self)
            self.machineCodeEdit = LineEdit(self)
            self.machine_code = get_machine_code()
            self.machineCodeEdit.setText(self.machine_code)
            self.machineCodeEdit.setReadOnly(True)
            self.actCodeLabel = StrongBodyLabel("激活码:", self)
            self.actCodeEdit = LineEdit(self)
            self.actButton = PrimaryPushButton(
                FluentIcon.DEVELOPER_TOOLS, "激活", self)
            self.machineCodeLayout = QHBoxLayout(self)
            self.machineCodeLayout.addWidget(self.machineCodeLabel)
            self.machineCodeLayout.addWidget(self.machineCodeEdit)
            self.actCodeLayout = QHBoxLayout(self)
            self.actCodeLayout.addWidget(self.actCodeLabel)
            self.actCodeLayout.addWidget(self.actCodeEdit)
            self.vBoxLayout.addLayout(self.machineCodeLayout)
            self.vBoxLayout.addLayout(self.actCodeLayout)
            self.vBoxLayout.addWidget(self.actButton)
            self.viewLayout.addLayout(self.vBoxLayout)
            self.actButton.clicked.connect(self.validate_activation_code)
            self.load_code()
            self.act_code = get_act_code()
            self.actCodeEdit.setText(self.act_code)

        def load_code(self):
            code = load_value("act_code")
            if code is not None:
                self.actCodeEdit.setText(code)

        def validate_activation_code(self):
            window = self.window()

            if DEV_MODE:
                print(self.act_code)

            if self.actCodeEdit.text().strip() == self.act_code:
                save_key_value("act_code", self.actCodeEdit.text().strip())
                window.activate_software()

    class SelectSpecializationCard(HeaderCardWidget):

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setTitle('专精选择')
            self.setBorderRadius(8)
            self.vBoxLayout = QVBoxLayout()
            self.hBoxLayout = QHBoxLayout()
            self.hBoxLayout.setSpacing(10)
            self.vBoxLayout.setSpacing(16)
            self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
            self.vBoxLayout.setContentsMargins(0, 0, 0, 0)
            if DEV_MODE:
                self.SPECIALIZATION = ["PriestDiscipline", "PriestShadow", "DemonHunterHavoc", "DemonHunterHavoc[Hekili]", "DemonHunterVengeance", "PriestDiscipline.OLD.4",
                                       "DeathKnightBlood", "DeathKnightUnholy",
                                       # "DeathKnightUnholy", "DruidBalance", "DruidFeral", "DruidGuardian", "DruidRestoration", "EvokerAugmentation",
                                       # "EvokerDevastation","EvokerPreservation", "HunterBeastMastery", "HunterMarksmanship", "HunterSurvival", "MageArcane", "MageFire", "MageFrost", "MonkBrewmaster", "MonkMistweaver", "MonkWindwalker",
                                       # "PaladinHoly","PaladinProtection", "PaladinRetribution", "PriestHoly", "PriestShadow", "RogueAssassination", "RogueOutlaw", "RogueSubtlety", "ShamanElemental", "ShamanEnhancement", "ShamanRestoration",
                                       # "WarlockAffliction","WarlockDemonology", "WarlockDestruction", "WarriorArms", "WarriorFury", "WarriorProtection",
                                       ]
            else:
                self.SPECIALIZATION = []
                for file in BASE_DIR.glob("*.rkf"):
                    self.SPECIALIZATION.append(file.stem)

            self.iconLabel = IconWidget(FluentIcon.INFO, self)
            self.iconLabel.setFixedSize(24, 24)
            self.comboBox = ComboBox(self)
            self.comboBox.addItems(self.SPECIALIZATION)
            self.comboBox.currentIndexChanged.connect(
                self.on_combo_box_changed)
            self.SelectButton = PushButton(FluentIcon.ACCEPT, "选定配置", self)
            self.SelectButton.clicked.connect(self.load_config)
            self.UnSelectButton = PushButton(FluentIcon.CANCEL, "解锁配置", self)
            self.UnSelectButton.setDisabled(True)

            self.hBoxLayout.addWidget(self.iconLabel, 1)
            self.hBoxLayout.addSpacing(8)
            self.hBoxLayout.addWidget(self.comboBox, 3)
            self.hBoxLayout.addWidget(self.SelectButton, 2)
            self.hBoxLayout.addWidget(self.UnSelectButton, 1)

            self.vBoxLayout.addLayout(self.hBoxLayout)
            self.viewLayout.addLayout(self.vBoxLayout)

        def on_combo_box_changed(self, index):
            selected_specialization = self.comboBox.currentText()
            print(f"Selected specialization: {selected_specialization}")

        def load_config(self):
            selected_specialization = self.comboBox.currentText()
            try:
                if DEV_MODE:
                    module = importlib.import_module(selected_specialization)
                    rotation_content = module.rotation_content
                    rotation_macros = module.rotation_macros
                    rotation_spell_list = module.spell_list
                    key_file = BASE_DIR.joinpath(
                        f"{selected_specialization}.rkf")
                    if key_file.exists():
                        key_file.unlink()
                    obj2file({"macros": rotation_macros,
                              "content": rotation_content,
                              "spell_list": rotation_spell_list}, key_file)
                else:
                    obj = file2obj(BASE_DIR.joinpath(
                        f"{selected_specialization}.rkf"))
                    rotation_macros = obj.get("macros")
                    rotation_content = obj.get("content")
                    rotation_spell_list = obj.get("spell_list")

                window = self.window()
                window.spellSettingInterface.import_card(rotation_spell_list)

                # print(rotation_content)
                rotation_content_macros = extract_prop_arguments(
                    rotation_content, "Cast")
                rotation_content_macros = sorted(
                    list(set(rotation_content_macros)))
                print(rotation_content_macros)
                i = 0
                macro_list = []
                for macro in rotation_content_macros:
                    if macro not in rotation_macros.keys():
                        return self.show_error("错误", f"配置文件中未找到{macro}")
                    macro_text = rotation_macros[macro]
                    macro_name = macro
                    macro_r = KEY_COLOR_MAP[i]['r']
                    macro_g = KEY_COLOR_MAP[i]['g']
                    macro_b = KEY_COLOR_MAP[i]['b']
                    macro_keybind = KEY_COLOR_MAP[i]['keybind']
                    i += 1
                    macro_list.append({
                        "macro_name": macro_name,
                        "macro_text": macro_text,
                        "macro_r": macro_r,
                        "macro_g": macro_g,
                        "macro_b": macro_b,
                        "macro_keybind": macro_keybind
                    })
                lua_02_macro = gen_macros_text(macro_list)
                lua_03_main = rotation_content
                lua_05_spell = gen_spell_text(rotation_spell_list)
                game_path = load_value("GamePath")
                if game_path is None:
                    return self.show_error("错误", "未找到游戏路径")
                game_path = Path(game_path)
                interface_path = game_path.joinpath(
                    "Interface").joinpath("AddOns").joinpath("Shion")
                if not interface_path.exists():
                    interface_path.mkdir(parents=True)
                with open(interface_path.joinpath("Shion.lua"), "w", encoding="utf-8") as f:
                    # lua_all = "\n".join([lua_01_header, lua_02_macro, lua_03_main, lua_04_footer, lua_05_spell])
                    lua_all = "\n".join(
                        [lua_01_header, lua_02_macro, lua_03_main, lua_04_footer, lua_05_spell])
                    f.write(lua_all)
                with open(interface_path.joinpath("Shion.toc"), "w", encoding="utf-8") as f:
                    f.write(toc_content)

            except AttributeError as e:
                print(e)
                return self.show_error("错误", "未找到配置文件，可能作者还没更新。")
            except ImportError as e:
                return self.show_error("错误", "未找到配置文件")
            print(f"Selected specialization: {selected_specialization}")

        def show_error(self, title, error):
            w = Dialog(title, error, self)
            w.yesButton.setText("我知道了")
            w.cancelButton.hide()
            w.buttonLayout.insertStretch(1)
            if w.exec():
                print('Yes button is pressed')
            else:
                print('Cancel button is pressed')

    class GamePathCard(HeaderCardWidget):
        def __init__(self, parent=None):
            super().__init__(parent)
            self.setTitle('游戏路径设置')
            self.setBorderRadius(8)

            self.gamePathIcon = IconWidget(FluentIcon.FOLDER, self)
            self.gamePathIcon.setFixedSize(24, 24)
            self.gamePathContent = BodyLabel("", self)
            self.gamePathSelectButton = PushButton("选择文件夹", self)
            self.gamePathSelectButton.clicked.connect(self.clicked_button)

            self.vBoxLayout = QVBoxLayout()
            self.hBoxLayout = QHBoxLayout()

            self.hBoxLayout.setSpacing(10)
            self.vBoxLayout.setSpacing(16)
            self.hBoxLayout.setContentsMargins(0, 0, 0, 0)
            self.vBoxLayout.setContentsMargins(0, 0, 0, 0)

            self.hBoxLayout.addWidget(self.gamePathIcon, 0, Qt.AlignLeft)
            self.hBoxLayout.addSpacing(16)
            self.hBoxLayout.addWidget(self.gamePathContent, 0, Qt.AlignLeft)
            self.hBoxLayout.addStretch(1)
            self.hBoxLayout.addWidget(
                self.gamePathSelectButton, 0, Qt.AlignLeft)
            self.vBoxLayout.addLayout(self.hBoxLayout)

            self.viewLayout.addLayout(self.vBoxLayout)
            self.load_config()

        def clicked_button(self):
            folder = QFileDialog.getExistingDirectory(
                self, "请选择目录", "./")
            if folder:
                if folder.endswith("_retail_"):
                    self.gamePathContent.setText(folder)
                    save_key_value("GamePath", folder)
                else:
                    w = Dialog("错误", "必须选择_retail_目录", self)
                    w.yesButton.setText("我知道了")
                    w.cancelButton.hide()
                    w.buttonLayout.insertStretch(1)
                    if w.exec():
                        print('Yes button is pressed')
                    else:
                        print('Cancel button is pressed')

        def load_config(self):
            game_path = load_value("GamePath")
            if game_path is not None:
                self.gamePathContent.setText(game_path)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.vBoxLayout.setSpacing(10)
        # self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("SettingInterface")
        self.activationCard = self.ActivationCard(self)

        self.vBoxLayout.addWidget(self.activationCard, 0, Qt.AlignTop)

        self.enableTransparentBackground()

    def activate_software(self):
        self.gamePathCard = self.GamePathCard(self)
        self.selectSpecializationCard = self.SelectSpecializationCard(self)
        self.vBoxLayout.addWidget(self.gamePathCard, 0, Qt.AlignTop)
        self.vBoxLayout.addWidget(
            self.selectSpecializationCard, 0, Qt.AlignTop)
        self.vBoxLayout.removeWidget(self.activationCard)
        self.activationCard.deleteLater()
        self.vBoxLayout.addStretch(1)


class SpellSettingInterface(ScrollArea):
    class EditCard(SimpleCardWidget):
        def __init__(self, title, placeholder, code, parent=None):
            super().__init__(parent)
            self.code = code
            self.setBorderRadius(8)
            self.vBoxLayout = QVBoxLayout(self)

            self.editLabel = BodyLabel(title, self)
            self.editInput = PlainTextEdit(self)
            self.editInput.setPlaceholderText(placeholder)

            self.saveButton = PushButton("保存", self)
            self.saveButton.setSizePolicy(
                QSizePolicy.Minimum, QSizePolicy.Expanding)
            self.saveButton.clicked.connect(self.save_config)

            self.L1Layout = QHBoxLayout()
            self.L1Layout.addWidget(self.editLabel, 1)
            self.L1Layout.addWidget(self.editInput, 4)
            self.L1Layout.addWidget(self.saveButton, 1)

            self.vBoxLayout.addLayout(self.L1Layout)
            self.load_config()

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
            spell_list = load_value(self.code, [])
            if spell_list is not None:
                spell_list = [str(spell) for spell in spell_list]
                self.editInput.setPlainText(", ".join(spell_list))

        def save_config(self):
            text = self.editInput.toPlainText()
            if self.check_input(self, text):
                spell_list = text.split(',')
                spell_list = [spell.strip() for spell in spell_list]
                spell_list = [spell for spell in spell_list if spell != '']
                spell_list = list(set(spell_list))
                spell_list = [int(spell) for spell in spell_list]
                spell_list.sort()
                save_key_value(self.code, spell_list)
            else:
                self.show_error("错误", "输入格式错误，必须是数字，用逗号分隔。")

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.view = QWidget(self)
        self.vBoxLayout = QVBoxLayout(self.view)
        self.vBoxLayout.setSpacing(10)
        # self.vBoxLayout.setAlignment(Qt.AlignTop)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("SpellSettingInterface")
        self.CardList = []

        self.vBoxLayout.addStretch(1)

        self.enableTransparentBackground()

    def clear_card(self):
        for card in self.CardList:
            self.vBoxLayout.removeWidget(card)
            card.deleteLater()
        self.CardList = []

    def import_card(self, card_list):
        for card in card_list:
            card_widget = self.EditCard(
                card["title"], card["placeholder"], card["code"], self)
            self.CardList.append(card_widget)
            self.vBoxLayout.insertWidget(0, card_widget, 0, Qt.AlignTop)


class RunningInterface(ScrollArea):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.view = QWidget(self)
        self.setWidget(self.view)
        self.setWidgetResizable(True)
        self.setObjectName("RunningInterface")

        self.vBoxLayout = QVBoxLayout(self.view)

        self.L1Layout = QHBoxLayout(self.view)
        self.L2Layout = QHBoxLayout(self.view)
        self.vBoxLayout.addLayout(self.L1Layout)
        self.vBoxLayout.addLayout(self.L2Layout)
        # self.vBoxLayout.addStretch(1)

        self.startBotButton = PrimaryPushButton(
            FluentIcon.PLAY, "开始", self.view)
        self.startBotButton.clicked.connect(self.start_bot)
        self.stopBotButton = PushButton(FluentIcon.PAUSE, "停止", self.view)
        self.stopBotButton.setDisabled(True)
        self.stopBotButton.clicked.connect(self.stop_bot)
        self.L1Layout.addWidget(self.startBotButton)
        self.L1Layout.addWidget(self.stopBotButton)

        self.log_text_edit = TextEdit(self.view)
        self.log_text_edit.setReadOnly(True)
        self.max_lines = 1000
        self.log_text_edit.setSizePolicy(
            QSizePolicy.Expanding, QSizePolicy.Expanding)
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
        self.worker.setup()
        self.worker.start()
        self.startBotButton.setDisabled(True)
        self.stopBotButton.setEnabled(True)

    def stop_bot(self):
        self.worker.stop_signal.emit()
        self.startBotButton.setEnabled(True)
        self.stopBotButton.setDisabled(True)

    def handle_output(self, output):
        if "error" in output:
            self.add_log(output["error"])
        else:
            self.add_log("按键：" + output["key_bind"] +
                         "  颜色:" + output["color"])


class Window(MSFluentWindow):

    def __init__(self):
        super().__init__()

        mutex_name = "Global\\ShionMutex"

        # 创建或打开互斥锁
        mutex = ctypes.windll.kernel32.CreateMutexW(None, False, mutex_name)

        # 检查互斥锁的返回值
        if ctypes.windll.kernel32.GetLastError() == 183:
            self.show_error("错误", "程序已运行，请关闭其他程序。")
            sys.exit()

        # create sub interface
        self.settingInterface = SettingInterface(self)
        # self.settingInterface = Widget('Setting Interface', self)
        self.spellSettingInterface = SpellSettingInterface(self)
        self.runningInterface = RunningInterface(self)
        # self.libraryInterface = Widget('library Interface', self)

        self.initNavigation()
        self.initWindow()

    def show_error(self, title, error):
        w = Dialog(title, error, self)
        w.yesButton.setText("我知道了")
        w.cancelButton.hide()
        w.buttonLayout.insertStretch(1)
        if w.exec():
            print('Yes button is pressed')
        else:
            print('Cancel button is pressed')

    def initNavigation(self):
        self.addSubInterface(self.settingInterface, FluentIcon.SETTING, '设置')
        self.addSubInterface(self.spellSettingInterface,
                             FluentIcon.APPLICATION, '技能设置')
        self.addSubInterface(self.runningInterface, FluentIcon.PLAY, '启动')

        self.navigationInterface.setCurrentItem(
            self.settingInterface.objectName())

    def initWindow(self):
        self.resize(900, 700)

        image_data = base64.b64decode(logo_data_base64)
        pixmap = QPixmap()
        pixmap.loadFromData(QByteArray(image_data))
        icon = QIcon(pixmap)
        self.setWindowIcon(icon)

        t = generate_unique_strings(4, 4)

        self.setWindowTitle("-".join(t))

        desktop = QApplication.screens()[0].availableGeometry()
        w, h = desktop.width(), desktop.height()
        self.move(w // 2 - self.width() // 2, h // 2 - self.height() // 2)

    def activate_software(self):
        self.settingInterface.activate_software()


if __name__ == '__main__':
    # setTheme(Theme.AUTO)
    init_config()
    app = QApplication(sys.argv)
    w = Window()
    w.show()
    app.exec()
