# core/clipboard_logger.py

import time
import threading
from datetime import datetime
import pyperclip

from core.app_tracker import get_active_window_info

class ClipboardLogger:
    def __init__(self, callback=None, poll_interval=1.0):
        self.last_clipboard = None
        self.callback = callback
        self.poll_interval = poll_interval
        self.running = False

    def poll_clipboard(self):
        while self.running:
            try:
                current_clipboard = pyperclip.paste()
                if current_clipboard != self.last_clipboard:
                    self.last_clipboard = current_clipboard
                    window_info = get_active_window_info()
                    event = {
                        'timestamp': datetime.utcnow().isoformat(),
                        'clipboard': current_clipboard,
                        'window': window_info['title'],
                        'process': window_info['process'],
                        'user': window_info.get('user', None)
                    }
                    if self.callback:
                        self.callback(event)
            except Exception as e:
                # Optionally log error
                pass
            time.sleep(self.poll_interval)

    def start(self):
        self.running = True
        t = threading.Thread(target=self.poll_clipboard, daemon=True)
        t.start()
        return t

    def stop(self):
        self.running = False

if __name__ == "__main__":
    def print_event(event):
        print(event)
    cl = ClipboardLogger(callback=print_event)
    cl.start()
    while True:
        time.sleep(10) 