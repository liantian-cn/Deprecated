import time
import random
import dxcam
from PIL import Image
import pyautogui
import keyboard

dx_camera = dxcam.create(device_idx=0, output_idx=0, output_color="RGB")

region = (0, 0, 32, 32)

dx_camera.start(region=region, video_mode=True, target_fps=120)

# 标志变量
continue_loop = True


# def star_loop():
#     print("开始")
#     global continue_loop
#     continue_loop = True
#
#
# def stop_loop():
#     print("停止")
#     global continue_loop
#     continue_loop = False


# keyboard.add_hotkey('alt+q', star_loop)
# keyboard.add_hotkey('alt+e', stop_loop)

while True:
    time.sleep(random.uniform(0.15, 0.25))
    # if not continue_loop:
    #
    #     continue
    frame = dx_camera.get_latest_frame()
    img = Image.fromarray(frame)
    pixel_color = img.getpixel((8, 16))
    pixel_color2 = img.getpixel((24, 16))
    if pixel_color != pixel_color2:
        print("不在程序")
    elif pixel_color == (255, 255, 255):
        print("闲置")
    elif pixel_color == (0, 0, 0):
        print("闲置")
    elif pixel_color == (0, 0, 128):
        print("死神的抚摩")
        pyautogui.press("3")
        # pyautogui.press("num1")
    elif pixel_color == (0, 0, 255):
        print("精髓分裂")
        pyautogui.hotkey('alt', 'q')
        # pyautogui.press("num2")
    elif pixel_color == (0, 128, 0):
        print("血液沸腾")
        pyautogui.hotkey('alt', '`')
        # pyautogui.press("num3")
    elif pixel_color == (0, 128, 128):
        print("灵界打击")
        pyautogui.press("e")
        # pyautogui.press("num4")
    elif pixel_color == (0, 128, 255):
        print("死神印记")
        pyautogui.hotkey('alt', 'e')
        # pyautogui.press("num5")
    elif pixel_color == (0, 255, 0):
        print("心脏打击")
        # pyautogui.press("num6")
        pyautogui.press("q")
    elif pixel_color == (0, 255, 128):
        print("白骨风暴")
        pyautogui.hotkey('alt', '3')
        # pyautogui.press("num7")
    elif pixel_color == (0, 255, 255):
        print("吸血鬼之血")
        pyautogui.hotkey('alt', '5')
        # pyautogui.press("num8")
    elif pixel_color == (255, 0, 0):
        print("吞噬")
        pyautogui.hotkey('alt', '1')
        # pyautogui.press("num9")
    elif pixel_color == (255, 0, 128):
        print("墓石")
        pyautogui.hotkey('alt', '2')
        # pyautogui.press("add")
    elif pixel_color == (255, 0, 255):
        print("枯萎凋零")
        pyautogui.press("5")
        # pyautogui.press("subtract")
    elif pixel_color == (255, 128, 0):
        print("心灵冰冻")
        # pyautogui.press("multiply")
        pyautogui.press("`")
    elif pixel_color == (255, 128, 128):
        print("加血护腕")   
        # pyautogui.press("multiply")
        pyautogui.hotkey('alt', 'X')
