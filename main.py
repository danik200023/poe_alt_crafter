import pyclip
from pynput.mouse import Listener, Button
import pyautogui


block_left_click = False


def on_click(x, y, button, pressed):
    global block_left_click

    if button == Button.left and block_left_click:
        return False


def analyze_item_description():
    item_description = pyclip.paste().decode("UTF-8")
    if "+1 to Level of all Skill Gems" in item_description:
        print("Mouse blocked")
        block_left_click = True


clipboard_content = pyclip.paste()

listener = Listener(on_click=on_click)
listener.start()

pyautogui.keyDown('shift')

while True:
    if pyclip.paste() != clipboard_content:
        clipboard_content = pyclip.paste()
        analyze_item_description()
    pyautogui.click()
    pyautogui.hotkey("ctrl", "c")
