# detection/script_detector.py

import re
import os
from typing import List, Callable

class ScriptDetector:
    def __init__(self, keyword_file='config/keywords.txt', ml_model=None, alert_callback: Callable = None):
        self.keywords = self.load_keywords(keyword_file)
        self.keyword_patterns = [re.compile(rf'\b{re.escape(word)}\b', re.IGNORECASE) for word in self.keywords]
        self.ml_model = ml_model  # Placeholder for ML model (e.g., XGBoost)
        self.alert_callback = alert_callback

    def load_keywords(self, filepath: str) -> List[str]:
        if not os.path.exists(filepath):
            return []
        with open(filepath, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f if line.strip() and not line.startswith('#')]

    def signature_detect(self, text: str) -> List[str]:
        """Return list of matched keywords in the text."""
        matches = []
        for pattern, word in zip(self.keyword_patterns, self.keywords):
            if pattern.search(text):
                matches.append(word)
        return matches

    def ml_detect(self, event) -> bool:
        """Stub for ML-based detection. Returns True if suspicious."""
        if self.ml_model is None:
            return False
        # Example: return self.ml_model.predict(event) == 1
        return False

    def process_event(self, event):
        """Process a keystroke event. Trigger alert if suspicious."""
        text = event.get('key', '')
        matches = self.signature_detect(text)
        ml_flag = self.ml_detect(event)
        if matches or ml_flag:
            alert = {
                'timestamp': event['timestamp'],
                'type': 'script_detection',
                'matches': matches,
                'ml_flag': ml_flag,
                'event': event
            }
            if self.alert_callback:
                self.alert_callback(alert)
            return alert
        return None

if __name__ == "__main__":
    def print_alert(alert):
        print(f"ALERT: {alert}")
    detector = ScriptDetector(alert_callback=print_alert)
    # Simulate keystroke events
    test_events = [
        {'timestamp': '2024-06-01T12:00:00Z', 'key': 'sudo rm -rf /', 'window': 'Terminal', 'process': 'bash', 'user': 'alice'},
        {'timestamp': '2024-06-01T12:01:00Z', 'key': 'hello world', 'window': 'Editor', 'process': 'vim', 'user': 'bob'},
    ]
    for event in test_events:
        detector.process_event(event)
