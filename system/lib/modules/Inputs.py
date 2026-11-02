import keyboard
import pyautogui
import time
from dataclasses import dataclass
from typing import Callable

@dataclass
class Vector2:
    x: float
    y: float

held_keys = set()
held_mouse_buttons = set()


def pressKey(key: str, delay: float = 0):
    time.sleep(delay)
    keyboard.press(key)
    held_keys.add(key)


def releaseKey(key: str, delay: float = 0):
    time.sleep(delay)
    keyboard.release(key)
    held_keys.discard(key)


def leftMouseDown(position: Vector2 = Vector2(1920 / 2, 1080 / 2), delay: float = 0):
    time.sleep(delay)
    pyautogui.moveTo(position.x, position.y)
    pyautogui.mouseDown(button="left")
    held_mouse_buttons.add("left")


def leftMouseUp(position: Vector2 = Vector2(1920 / 2, 1080 / 2), delay: float = 0):
    time.sleep(delay)
    pyautogui.mouseUp(button="left")
    held_mouse_buttons.discard("left")


def releaseAllInputs():
    for key in held_keys.copy():
        try:
            keyboard.release(key)
        except Exception:
            pass
    held_keys.clear()

    for button in held_mouse_buttons.copy():
        try:
            pyautogui.mouseUp(button=button)
        except Exception:
            pass
    held_mouse_buttons.clear()


def onKeyPress(BOT_ID, key: str, callback: Callable[[str, str], None]):
    def handler(event):
        if event.name == key:
            callback(BOT_ID)

    keyboard.on_press(handler)