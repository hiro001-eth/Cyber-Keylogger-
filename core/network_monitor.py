# core/network_monitor.py

import threading
import time
import psutil
from datetime import datetime

class NetworkMonitor:
    def __init__(self, callback=None, poll_interval=5):
        self.callback = callback
        self.poll_interval = poll_interval
        self.running = False

    def poll_network(self):
        while self.running:
            for conn in psutil.net_connections(kind='inet'):
                if conn.status == 'ESTABLISHED':
                    event = {
                        'timestamp': datetime.utcnow().isoformat(),
                        'laddr': str(conn.laddr),
                        'raddr': str(conn.raddr) if conn.raddr else None,
                        'pid': conn.pid,
                        'process': psutil.Process(conn.pid).name() if conn.pid else None
                    }
                    if self.callback:
                        self.callback(event)
            time.sleep(self.poll_interval)

    def start(self):
        self.running = True
        t = threading.Thread(target=self.poll_network, daemon=True)
        t.start()
        return t

    def stop(self):
        self.running = False
