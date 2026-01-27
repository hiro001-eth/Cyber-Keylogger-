# tests/test_keylogger.py

import unittest
from core.keylogger import KeyLogger

class TestKeyLogger(unittest.TestCase):
    def test_keystroke_event(self):
        events = []
        kl = KeyLogger(callback=lambda e: events.append(e))
        kl.on_press(type('Key', (), {'char': 'a'})())
        self.assertEqual(events[0]['key'], 'a')
        self.assertIn('timestamp', events[0])

if __name__ == '__main__':
    unittest.main()
