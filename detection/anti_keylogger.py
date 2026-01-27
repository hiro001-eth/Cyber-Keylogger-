# detection/anti_keylogger.py

import psutil
import re
from datetime import datetime

SUSPICIOUS_PATTERNS = [
    re.compile(r'keylog', re.IGNORECASE),
    re.compile(r'pynput', re.IGNORECASE),
    re.compile(r'hook', re.IGNORECASE)
]

def scan_for_keyloggers():
    alerts = []
    for proc in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
        try:
            name = proc.info['name'] or ''
            cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
            for pattern in SUSPICIOUS_PATTERNS:
                if pattern.search(name) or pattern.search(cmdline):
                    alerts.append({
                        'timestamp': datetime.utcnow().isoformat(),
                        'pid': proc.info['pid'],
                        'name': name,
                        'cmdline': cmdline,
                        'reason': f"Matched pattern: {pattern.pattern}"
                    })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    return alerts

if __name__ == '__main__':
    for alert in scan_for_keyloggers():
        print(alert)
