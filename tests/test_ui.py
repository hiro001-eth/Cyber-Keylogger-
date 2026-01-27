# tests/test_ui.py

import unittest
from ui.user_guide import log_consent

class TestUI(unittest.TestCase):
    def test_log_consent(self):
        log_consent(user="testuser")
        with open('logs/consent.log', 'r', encoding='utf-8') as f:
            lines = f.readlines()
        self.assertTrue(any("testuser" in line for line in lines))

if __name__ == '__main__':
    unittest.main()
