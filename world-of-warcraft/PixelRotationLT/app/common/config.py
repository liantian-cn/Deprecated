from app.common.cipher import obj2file, file2obj
from app.common.utils import BASE_DIR
CONFIG_FILE = BASE_DIR.joinpath("config.db")


def init_config():
    cfg = {
        "profiles": {},
        "GamePath": "X:/World of Warcraft/_retail_",
        "act_code": "",
        "username": "",
        "snippets": {},
        "interrupt_spell_list": [],
        "interrupt_black_list": [],
        "important_spell_list": []
    }
    if not CONFIG_FILE.exists():
        obj2file(cfg, CONFIG_FILE)


def load_profile(profile_name=None):
    cfg = file2obj(CONFIG_FILE)
    if profile_name is None:
        return cfg["profiles"]
    else:
        profile = cfg["profiles"].get(profile_name, None)
        return profile


def save_profile(profile_name, profile):
    cfg = file2obj(CONFIG_FILE)
    cfg["profiles"][profile_name] = profile
    obj2file(cfg, CONFIG_FILE)


def load_value(key, default=None):
    cfg = file2obj(CONFIG_FILE)
    return cfg.get(key, default)  # 如果key不存在，返回None


def save_key_value(key, value):
    cfg = file2obj(CONFIG_FILE)
    cfg[key] = value
    obj2file(cfg, CONFIG_FILE)


# def save_snippet(snippet_name, code):
#     cfg = file2obj(CONFIG_FILE)
#     if "snippets" not in cfg:
#         cfg["snippets"] = {}
#     cfg["snippets"][snippet_name] = code
#     obj2file(cfg, CONFIG_FILE)
#
#
# def load_snippet(snippet_name):
#     cfg = file2obj(CONFIG_FILE)
#     return cfg["snippets"].get(snippet_name, None)
#
#
# def list_snippets():
#     cfg = file2obj(CONFIG_FILE)
#     if "snippets" not in cfg:
#         cfg["snippets"] = {}
#     return cfg["snippets"].keys()
