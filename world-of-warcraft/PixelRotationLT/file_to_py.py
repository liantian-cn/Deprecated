import os
import zlib
import base64
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def compress_and_encode_file():
    # 隐藏主窗口
    root = Tk()
    root.withdraw()  # 不显示主窗口
    # 打开文件对话框，选择文件
    file_path = askopenfilename(title="选择一个文件", filetypes=[("所有文件", "*.*")])

    if not file_path:
        print("未选择文件。")
        return
    base_file_name = os.path.basename(file_path)
    file_name, _ = os.path.splitext(base_file_name)
    output_file = f"{file_name}.py"

    # 读取文件内容
    with open(file_path, 'rb') as input_file:
        file_data = input_file.read()

        # 使用 zlib 进行压缩
    compressed_data = zlib.compress(file_data,level=9)

    # 使用 base64 编码
    encoded_data = base64.b64encode(compressed_data).decode('utf-8')

    # 将 Base64 数据保存到 Python 文件中
    with open(output_file, 'w') as py_file:
        py_file.write("image_data = '''\n")
        max_line_length = 76
        for i in range(0, len(encoded_data), max_line_length):
            py_file.write(encoded_data[i:i + max_line_length] + '\n')
        py_file.write("'''\n")

    print(f"Base64 编码数据已保存到 {output_file}。")


if __name__ == "__main__":
    compress_and_encode_file()
