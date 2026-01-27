# tests/test_detection.py

import unittest
from detection.script_detector import ScriptDetector
from detection.anomaly_detector import AnomalyDetector

class TestDetection(unittest.TestCase):
    def test_script_signature(self):
        detector = ScriptDetector(keyword_file="config/keywords.txt")
        event = {'timestamp': '2024-01-01T00:00:00Z', 'key': 'sudo rm -rf /', 'window': 'Terminal', 'process': 'bash', 'user': 'alice'}
        alert = detector.process_event(event)
        self.assertIsNotNone(alert)
        self.assertIn('sudo', alert['matches'])

    def test_anomaly_detection(self):
        detector = AnomalyDetector()
        # Simulate rapid, uniform keystrokes
        import time
        base = time.time()
        for i in range(12):
            event = {
                'timestamp': time.strftime('%Y-%m-%dT%H:%M:%S', time.localtime(base + i * 0.01)),
                'key': 'a',
                'window': 'Terminal',
                'process': 'python',
                'user': 'alice'
            }
            alert = detector.process_event(event)
        self.assertIsNotNone(alert)

if __name__ == '__main__':
    unittest.main()
