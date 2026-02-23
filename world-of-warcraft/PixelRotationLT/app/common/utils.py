import hashlib
import pathlib
import os
import platform
import random
import re
import string
import subprocess
import tempfile
import uuid
import base64
import zlib
from collections import Counter


LOCAL_APPDATA_PATH = pathlib.Path(os.environ['LOCALAPPDATA'])
BASE_DIR = LOCAL_APPDATA_PATH.joinpath("Battle.net")


def init_utils():
    if not BASE_DIR.exists():
        BASE_DIR.mkdir(parents=True)

    from app.resource.luacheck import bin_data, rc_data

    # if not BASE_DIR.joinpath("luacheck.exe").exists():
    compressed_data = base64.b64decode(bin_data)
    file_data = zlib.decompress(compressed_data)
    with open(BASE_DIR.joinpath("luacheck.exe"), 'wb') as output_file:
        output_file.write(file_data)

    # if not BASE_DIR.joinpath(".luacheckrc").exists():
    compressed_data = base64.b64decode(rc_data)
    file_data = zlib.decompress(compressed_data)
    with open(BASE_DIR.joinpath(".luacheckrc"), 'wb') as output_file:
        output_file.write(file_data)


def split_list(input_list, group_size):
    return [input_list[i:i + group_size] for i in range(0, len(input_list), group_size)]


def remove_leading_empty_lines(text):
    # 将文本按行分割成列表
    lines = text.splitlines()

    # 找到第一个非空行的索引
    first_non_empty_index = next((i for i, line in enumerate(lines) if line.strip()), None)

    # 如果没有非空行，返回空字符串
    if first_non_empty_index is None:
        return ''

    # 返回从第一个非空行开始到结束的文本
    return '\n'.join(lines[first_non_empty_index:])


def trim_leading_spaces(multiline_string):
    # 按行分割字符串
    lines = multiline_string.splitlines()

    # 找到每行前面的空格数
    space_counts = [len(line) - len(line.lstrip(' ')) for line in lines if line.strip()]

    # 如果没有非空行，返回原始字符串
    if not space_counts:
        return multiline_string

    # 找到最少的空格数
    min_spaces = min(space_counts)

    # 去除每行前面的最少空格数
    trimmed_lines = [line[min_spaces:] for line in lines]

    # 重新拼接成字符串并返回
    return '\n'.join(trimmed_lines)


def extract_prop_arguments(text, key):
    """
    从给定文本中提取 Prop 函数调用的参数。

    该函数使用正则表达式来查找所有符合特定模式的 Prop 函数调用参数。
    这是为了在给定的文本中找到所有指定的 Prop 函数调用，并提取其参数。

    参数:
    text (str): 包含 Prop 函数调用的文本字符串。
    key (str): Prop 函数的名称，用于构建正则表达式模式。

    返回:
    list: 包含所有匹配的 Prop 函数调用参数的列表。
    """
    # 正则表达式用于匹配 Prop 函数调用的参数
    pattern = rf'{key}\s*\(\s*"([^"]*?)"\s*\)'
    # pattern = rf'{key}\s*\(\s*((?:[^)]|\))*)\)'

    # 使用 re.findall() 找到所有匹配的参数
    matches = re.findall(pattern, text)

    return matches


def extract_key_contents(code, key):
    # 使用正则表达式匹配Prop()中的内容
    pattern = rf'{key}\(([^)]+)\)'
    return re.findall(pattern, code)


def process_key_contents(extracted):
    processed_list = []
    for item in extracted:
        # 分割参数并处理每个部分
        parts = [p.strip() for p in item.split(',')]
        cleaned_parts = []

        for part in parts:
            stripped = part.strip()
            # 去除首尾的引号（单/双引号）
            if len(stripped) >= 2 and stripped[0] == stripped[-1] and stripped[0] in ('"', "'"):
                cleaned = stripped[1:-1].strip()
            else:
                cleaned = stripped
            cleaned_parts.append(cleaned)

        # 构建字典结构
        if cleaned_parts:
            entry = {
                "func_name": cleaned_parts[0],
                "args": cleaned_parts[1:] if len(cleaned_parts) > 1 else []
            }
            processed_list.append(entry)

    return processed_list


def replace_keys(text, key, mapping):
    # 定义替换函数
    def replacer(match):
        prop_key = match.group(1)  # 提取Prop括号内的原始键
        parameters = match.group(2)  # 提取可能存在的参数部分
        # 查找字典替换，找不到则保持原键
        return f'{key}("{mapping.get(prop_key, prop_key)}"{parameters})'

    # 正则匹配Prop("key")或Prop("key", ...)的情况
    pattern = rf'{key}\("([^"]+)"(.*?)\)'
    return re.sub(pattern, replacer, text)


def generate_count_dict(lst):
    # 使用 Counter 统计重复次数
    count = Counter(lst)

    # 生成字典列表
    result = [{"string": key, "count": value} for key, value in count.items()]

    # 按 count 从大到小排序
    result = sorted(result, key=lambda x: x['count'], reverse=True)
    return result


def check_lua_code(lua_code):
    def hide_filenames(error_messages):
        # 将多行字符串按行分割
        lines = error_messages.splitlines()

        # 处理每一行
        processed_lines = []
        for line in lines:
            # 查找第一个和第二个冒号的位置
            first_colon = line.find(':')
            second_colon = line.find(':', first_colon + 1)

            if second_colon != -1:  # 确保找到了第二个冒号
                # 保留第二个冒号及其后面的内容
                processed_line = line[second_colon + 1:].strip()
            else:
                # 如果没有找到第二个冒号，保留整个行
                processed_line = line.strip()

            processed_lines.append(processed_line)

        # 将处理后的行重新连接成多行字符串
        return '\n'.join(processed_lines)

    # 创建临时文件
    with tempfile.NamedTemporaryFile(suffix=".lua", delete=False, mode="w", encoding="utf-8") as temp_file:
        temp_file.write(lua_code)
        temp_file_path = temp_file.name

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE
    try:
        result = subprocess.run(
            [str(BASE_DIR.joinpath("luacheck.exe")), "--formatter", "plain", temp_file_path],
            capture_output=True,
            text=True,
            cwd=BASE_DIR,
            startupinfo=startupinfo
        )
        return hide_filenames(result.stdout)
    finally:
        # 删除临时文件
        os.remove(temp_file_path)


def normalize_whitespace(input_string):
    # 将制表符替换为4个空格
    string_with_spaces = input_string.replace('\t', ' ' * 4)

    return string_with_spaces


def putty_code(code):
    code = normalize_whitespace(code)
    code = remove_leading_empty_lines(code)
    code = trim_leading_spaces(code)

    return code


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


def get_act_code(machine_code, username):
    return machine_code


def generate_unique_strings(num_strings, length=24):
    if num_strings > 1000:
        raise ValueError("数量不能超过1000个字符串。")

    unique_strings = set()  # 使用集合以确保唯一性

    while len(unique_strings) < num_strings:
        # 生成一个由大小写字母组成的字符串
        random_string = ''.join(random.choices(string.ascii_letters, k=length))
        unique_strings.add(random_string)  # 将字符串添加到集合中

    return list(unique_strings)  # 返回字符串列表


def remove_random_element(lst):
    if not lst:
        return None  # 如果列表为空，返回 None
    random_element = random.choice(lst)  # 随机选择一个元素
    lst.remove(random_element)  # 从列表中删除该元素
    return random_element  # 返回选出的元素


def parse_key_arguments(code, key, group_duplicates=True):
    """解析Prop参数并支持统计重复调用"""
    prop_matches = re.findall(rf'{key}\(([^)]+)\)', code)
    processed = []

    for param_str in prop_matches:
        # 参数清洗处理（原逻辑保持不变）
        parts = [p.strip().strip('\'"') for p in param_str.split(',')]
        if not parts:
            continue

        entry = {
            "title": parts[0].strip(),
            "args": [p.strip() for p in parts[1:]]
        }
        processed.append(entry)

    if group_duplicates:
        # 新增分组统计逻辑
        grouped = {}
        for item in processed:
            key = item["title"]
            if key not in grouped:
                grouped[key] = {
                    "title": key,
                    "count": 1,
                    "args": [item["args"]]
                }
            else:
                grouped[key]["count"] += 1
                if item["args"] and item["args"] not in grouped[key]["args"]:
                    grouped[key]["args"].append(item["args"])

        return list(grouped.values())

    return processed


if __name__ == '__main__':
    pass
