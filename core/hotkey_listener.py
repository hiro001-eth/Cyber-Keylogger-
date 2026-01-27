# core/hotkey_listener.py

from pynput import keyboard
import threading

class HotkeyListener:
    def __init__(self, on_hotkey):
        self.on_hotkey = on_hotkey
        self.listener = None

    def start(self):
        def for_canonical(f):
            return lambda k: f(self.listener.canonical(k))
        self.listener = keyboard.GlobalHotKeys({
            '<ctrl>+<alt>+p': self.on_hotkey
        })
        self.listener.start()
        return self.listener

    def stop(self):
        if self.listener:
            self.listener.stop()
