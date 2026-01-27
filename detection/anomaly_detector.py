# detection/anomaly_detector.py

import time
from typing import List, Callable

class AnomalyDetector:
    def __init__(self, ml_model=None, alert_callback: Callable = None, window_size=10, speed_threshold=0.05, uniformity_threshold=0.01):
        self.ml_model = ml_model  # Placeholder for ML model
        self.alert_callback = alert_callback
        self.window_size = window_size
        self.speed_threshold = speed_threshold  # Min interval (sec) for human typing
        self.uniformity_threshold = uniformity_threshold  # Max stddev for uniformity
        self.last_events = []  # Store (timestamp, key)

    def process_event(self, event):
        ts = self._parse_timestamp(event['timestamp'])
        self.last_events.append((ts, event['key']))
        if len(self.last_events) > self.window_size:
            self.last_events.pop(0)
        if len(self.last_events) >= 2:
            intervals = [self.last_events[i][0] - self.last_events[i-1][0] for i in range(1, len(self.last_events))]
            avg_interval = sum(intervals) / len(intervals)
            stddev = (sum((x - avg_interval) ** 2 for x in intervals) / len(intervals)) ** 0.5
            # Heuristic: very fast and uniform typing is suspicious
            is_fast = avg_interval < self.speed_threshold
            is_uniform = stddev < self.uniformity_threshold
            is_repetitive = len(set(k for _, k in self.last_events)) < self.window_size // 2
            ml_flag = self.ml_detect(event, intervals) if self.ml_model else False
            if (is_fast and is_uniform) or is_repetitive or ml_flag:
                alert = {
                    'timestamp': event['timestamp'],
                    'type': 'anomaly_detection',
                    'avg_interval': avg_interval,
                    'stddev': stddev,
                    'is_fast': is_fast,
                    'is_uniform': is_uniform,
                    'is_repetitive': is_repetitive,
                    'ml_flag': ml_flag,
                    'event': event
                }
                if self.alert_callback:
                    self.alert_callback(alert)
                return alert
        return None

    def ml_detect(self, event, intervals) -> bool:
        # Placeholder for ML-based anomaly detection
        # Example: return self.ml_model.predict([...]) == 1
        return False

    def _parse_timestamp(self, ts):
        # Accepts ISO format, returns float seconds
        try:
            return time.mktime(time.strptime(ts.split('.')[0], '%Y-%m-%dT%H:%M:%S'))
        except Exception:
            return time.time()

if __name__ == "__main__":
    def print_alert(alert):
        print(f"ANOMALY ALERT: {alert}")
    detector = AnomalyDetector(alert_callback=print_alert)
    # Simulate rapid, uniform keystrokes (scripted)
    base = time.time()
    for i in range(12):
        event = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(base + i * 0.01)),
            'key': 'a',
            'window': 'Terminal',
            'process': 'python',
            'user': 'alice'
        }
        detector.process_event(event)
    # Simulate normal human typing
    base = time.time()
    for i in range(12):
        event = {
            'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(base + i * 0.2)),
            'key': chr(97 + i),
            'window': 'Editor',
            'process': 'vim',
            'user': 'bob'
        }
        detector.process_event(event)
