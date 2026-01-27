# core/mouse_logger.py

import threading
import time
from datetime import datetime
from pynput import mouse
from core.app_tracker import get_active_window_info

class MouseLogger:
    def __init__(self, callback=None):
        self.callback = callback
        self.log = []
        self.listener = None

    def on_move(self, x, y):
        window_info = get_active_window_info()
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event': 'move',
            'position': (x, y),
            'window': window_info['title'],
            'process': window_info['process'],
            'user': window_info.get('user', None)
        }
        self.log.append(event)
        if self.callback:
            self.callback(event)

    def on_click(self, x, y, button, pressed):
        window_info = get_active_window_info()
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event': 'click',
            'position': (x, y),
            'button': str(button),
            'pressed': pressed,
            'window': window_info['title'],
            'process': window_info['process'],
            'user': window_info.get('user', None)
        }
        self.log.append(event)
        if self.callback:
            self.callback(event)

    def on_scroll(self, x, y, dx, dy):
        window_info = get_active_window_info()
        event = {
            'timestamp': datetime.utcnow().isoformat(),
            'event': 'scroll',
            'position': (x, y),
            'dx': dx,
            'dy': dy,
            'window': window_info['title'],
            'process': window_info['process'],
            'user': window_info.get('user', None)
        }
        self.log.append(event)
        if self.callback:
            self.callback(event)

    def start(self):
        self.listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click,
            on_scroll=self.on_scroll
        )
        self.listener.start()
        return self.listener

    def stop(self):
        if self.listener:
            self.listener.stop()

    def get_log(self):
        return self.log

if __name__ == "__main__":
    def print_event(event):
        print(event)
    ml = MouseLogger(callback=print_event)
    ml.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Mouse logger stopped.")
