import ctypes
import time
from pynput.mouse import Listener, Button
import pyautogui

# Определение функций и констант ctypes для доступа к буферу обмена Windows

CF_UNICODETEXT = 13

user32 = ctypes.windll.user32
kernel32 = ctypes.windll.kernel32

OpenClipboard = user32.OpenClipboard
CloseClipboard = user32.CloseClipboard
GetClipboardData = user32.GetClipboardData
EmptyClipboard = user32.EmptyClipboard
SetClipboardData = user32.SetClipboardData

GlobalLock = kernel32.GlobalLock
GlobalUnlock = kernel32.GlobalUnlock
GlobalAlloc = kernel32.GlobalAlloc
GlobalSize = kernel32.GlobalSize
memcpy = ctypes.cdll.msvcrt.memcpy

GMEM_MOVEABLE = 0x0002
GMEM_ZEROINIT = 0x0040


def get_clipboard_text():
    # Открытие буфера обмена
    OpenClipboard(None)

    # Получение дескриптора данных буфера обмена
    h_clipboard = GetClipboardData(CF_UNICODETEXT)

    # Блокировка дескриптора и получение указателя на данные
    locked_clipboard = GlobalLock(h_clipboard)
    p_clipboard = ctypes.c_char_p(locked_clipboard)

    # Определение размера данных буфера обмена
    size = GlobalSize(h_clipboard)

    # Создание буфера и копирование данных
    buffer = ctypes.create_string_buffer(size)
    memcpy(buffer, p_clipboard, size)

    # Разблокировка дескриптора
    GlobalUnlock(h_clipboard)

    # Закрытие буфера обмена
    CloseClipboard()

    # Декодирование буфера в строку и возврат текста
    return buffer.value.decode("utf-8")


def set_clipboard_text(text):
    # Открытие буфера обмена
    OpenClipboard(None)

    # Очистка буфера обмена
    EmptyClipboard()

    # Получение размера буфера для текста
    size = len(text.encode("utf-8"))

    # Выделение памяти для буфера и копирование текста
    h_global = GlobalAlloc(GMEM_MOVEABLE | GMEM_ZEROINIT, size)
    locked_global = GlobalLock(h_global)
    memcpy(locked_global, text.encode("utf-8"), size)
    GlobalUnlock(h_global)

    # Установка данных буфера обмена
    SetClipboardData(CF_UNICODETEXT, h_global)

    # Закрытие буфера обмена
    CloseClipboard()


block_left_click = False


def on_click(x, y, button, pressed):
    global block_left_click

    if button == Button.left and block_left_click:
        return False


def analyze_item_description():
    item_description = get_clipboard_text()
    if "+1 to Level of all Skill Gems" in item_description:
        print("Mouse blocked")
        block_left_click = True


clipboard_content = get_clipboard_text()

listener = Listener(on_click=on_click)
listener.start()

pyautogui.keyDown('shift')

while True:
    if get_clipboard_text() != clipboard_content:
        clipboard_content = get_clipboard_text()
        analyze_item_description()
    pyautogui.click()
    pyautogui.hotkey("ctrl", "c")
