
import os
import time
import threading
from datetime import datetime
from core.app_tracker import get_active_window_info

try:
    import mss
    from PIL import Image
except ImportError:
    raise ImportError("Please install 'mss' and 'Pillow' for screen capture functionality.")

class ScreenCapture:
    def __init__(self, screenshot_dir='logs/screenshots', interval=60, callback=None):
        self.screenshot_dir = screenshot_dir
        self.interval = interval
        self.callback = callback
        self.running = False
        os.makedirs(self.screenshot_dir, exist_ok=True)

    def capture_screenshot(self):
        with mss.mss() as sct:
            monitor = sct.monitors[1]
            img = sct.grab(monitor)
            img_pil = Image.frombytes('RGB', img.size, img.rgb)
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            window_info = get_active_window_info()
            filename = f"{timestamp}_{window_info['process'] or 'unknown'}.png"
            filepath = os.path.join(self.screenshot_dir, filename)
            img_pil.save(filepath)
            event = {
                'timestamp': timestamp,
                'filepath': filepath,
                'window': window_info['title'],
                'process': window_info['process'],
                'user': window_info.get('user', None)
            }
            if self.callback:
                self.callback(event)
            return event

    def start(self):
        self.running = True
        t = threading.Thread(target=self._run, daemon=True)
        t.start()
        return t

    def stop(self):
        self.running = False

    def _run(self):
        while self.running:
            try:
                self.capture_screenshot()
            except Exception:
                pass
            time.sleep(self.interval)

if __name__ == "__main__":
    def print_event(event):
        print(f"Screenshot taken: {event}")
    sc = ScreenCapture(interval=10, callback=print_event)
    sc.start()
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("Screen capture stopped.")

