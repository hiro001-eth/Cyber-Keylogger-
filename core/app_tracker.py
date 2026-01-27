# core/app_tracker.py

import sys
import time

def get_active_window_info():
    if sys.platform.startswith('win'):
        import win32gui
        import win32process
        import psutil
        hwnd = win32gui.GetForegroundWindow()
        pid = win32process.GetWindowThreadProcessId(hwnd)[1]
        process = psutil.Process(pid)
        return {
            'title': win32gui.GetWindowText(hwnd),
            'process': process.name(),
            'user': process.username()
        }
    elif sys.platform.startswith('darwin'):
        from AppKit import NSWorkspace
        active_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        return {
            'title': active_app.localizedName(),
            'process': active_app.bundleIdentifier(),
            'user': None
        }
    elif sys.platform.startswith('linux'):
        try:
            import subprocess
            win_id = subprocess.check_output(['xdotool', 'getactivewindow']).strip()
            win_name = subprocess.check_output(['xdotool', 'getwindowname', win_id]).decode().strip()
            pid = subprocess.check_output(['xdotool', 'getwindowpid', win_id]).strip()
            proc_name = subprocess.check_output(['ps', '-p', pid, '-o', 'comm=']).decode().strip()
            return {
                'title': win_name,
                'process': proc_name,
                'user': None
            }
        except Exception:
            return {'title': None, 'process': None, 'user': None}
    else:
        return {'title': None, 'process': None, 'user': None}

class AppUsageTracker:
    def __init__(self, callback=None, poll_interval=5):
        self.callback = callback
        self.poll_interval = poll_interval
        self.running = False
        self.current_app = None
        self.start_time = None

    def poll(self):
        while self.running:
            info = get_active_window_info()
            app = info['process']
            now = time.time()
            if app != self.current_app:
                if self.current_app and self.start_time:
                    duration = now - self.start_time
                    event = {
                        'app': self.current_app,
                        'duration': duration,
                        'end_time': now
                    }
                    if self.callback:
                        self.callback(event)
                self.current_app = app
                self.start_time = now
            time.sleep(self.poll_interval)

    def start(self):
        import threading
        self.running = True
        t = threading.Thread(target=self.poll, daemon=True)
        t.start()
        return t

    def stop(self):
        self.running = False