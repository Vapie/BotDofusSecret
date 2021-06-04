import time

import pyautogui
import pygetwindow
import subprocess
import os

def screenshot_screen(x1: int,y1: int,x2: int,y2: int,is_saved_image: bool,name: str =""):
    my_screenshot = pyautogui.screenshot(region=(x1,y1,x2,y2))
    if(is_saved_image):
        my_screenshot.save(r'./screenshots/'+name)
    return my_screenshot
def resize_window(window_name: str,window_width: int,window_height: int) -> None:
    win = pygetwindow.getWindowsWithTitle(window_name)[0]
    win.size = (window_width, window_height)

def move_window(window_name: str,window_x: int,window_y: int) -> None:
    win = pygetwindow.getWindowsWithTitle(window_name)[0]
    win.moveTo(window_x, window_y)

def lauch_app(path: str) -> None:
    print(path)
    os.startfile(path)

def is_subitem_on_screen(image_path: str):
    return True

def launch_app_with_size(path: str,app_name: str,width: int, height: int,sub_image_path_of_app_when_started: str = "") -> None:
    lauch_app(path)
    time.sleep(5)
    if(sub_image_path_of_app_when_started != ""):
        while not is_subitem_on_screen(sub_image_path_of_app_when_started):
            time.sleep(1)
    resize_window(app_name,width,height)


