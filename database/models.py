# Add to database/models.py

import sqlite3
from datetime import datetime
from typing import Optional, List, Dict, Any
import json
import hashlib
import secrets

class DatabaseModels:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()
    
    def hash_password(self, password: str) -> str:
        """Hash password using PBKDF2"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 600000)
        return f"pbkdf2:sha256:600000${salt}${hash_obj.hex()}"
    
    def init_database(self):
        """Initialize all database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Users table (Admin and Employees)
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    email VARCHAR(100) UNIQUE NOT NULL,
                    password_hash VARCHAR(255) NOT NULL,
                    role VARCHAR(20) NOT NULL CHECK (role IN ('admin', 'employee')),
                    employee_code VARCHAR(10) UNIQUE,
                    company_id VARCHAR(50),
                    department VARCHAR(50),
                    position VARCHAR(50),
                    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'inactive', 'suspended')),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    last_login TIMESTAMP,
                    consent_given BOOLEAN DEFAULT FALSE,
                    consent_date TIMESTAMP,
                    created_by INTEGER,
                    FOREIGN KEY (created_by) REFERENCES users(id)
                )
            ''')
            
            # Companies table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS companies (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name VARCHAR(100) NOT NULL,
                    domain VARCHAR(100) UNIQUE,
                    license_key VARCHAR(255),
                    subscription_plan VARCHAR(50),
                    max_employees INTEGER DEFAULT 100,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status VARCHAR(20) DEFAULT 'active'
                )
            ''')
            
            # Keystrokes table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS keystrokes (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    key_pressed VARCHAR(10),
                    key_code INTEGER,
                    window_title VARCHAR(255),
                    application_name VARCHAR(100),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_sensitive BOOLEAN DEFAULT FALSE,
                    context_data TEXT,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Mouse events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS mouse_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    event_type VARCHAR(20),
                    x_position INTEGER,
                    y_position INTEGER,
                    button VARCHAR(10),
                    window_title VARCHAR(255),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Clipboard events table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS clipboard_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    content_hash VARCHAR(64),
                    content_preview VARCHAR(255),
                    window_title VARCHAR(255),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_sensitive BOOLEAN DEFAULT FALSE,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Screen captures table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS screen_captures (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    file_path VARCHAR(255),
                    file_size INTEGER,
                    window_title VARCHAR(255),
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    trigger_type VARCHAR(50),
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Alerts table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    alert_type VARCHAR(50),
                    severity VARCHAR(20),
                    message TEXT,
                    context_data TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    is_resolved BOOLEAN DEFAULT FALSE,
                    resolved_by INTEGER,
                    resolved_at TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (resolved_by) REFERENCES users(id)
                )
            ''')
            
            # Activity sessions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS activity_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    session_start TIMESTAMP,
                    session_end TIMESTAMP,
                    total_keystrokes INTEGER DEFAULT 0,
                    total_mouse_clicks INTEGER DEFAULT 0,
                    applications_used TEXT,
                    productivity_score FLOAT,
                    idle_time_minutes INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                )
            ''')
            
            # Audit log table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS audit_log (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    admin_id INTEGER NOT NULL,
                    action_type VARCHAR(50),
                    target_user_id INTEGER,
                    details TEXT,
                    ip_address VARCHAR(45),
                    user_agent TEXT,
                    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (admin_id) REFERENCES users(id),
                    FOREIGN KEY (target_user_id) REFERENCES users(id)
                )
            ''')
            
            # Settings table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS settings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    setting_key VARCHAR(100) UNIQUE NOT NULL,
                    setting_value TEXT,
                    description TEXT,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_by INTEGER,
                    FOREIGN KEY (updated_by) REFERENCES users(id)
                )
            ''')
            
            # Create default super admin user with proper password hash
            admin_password_hash = self.hash_password('admin123')
            cursor.execute('''
                INSERT OR IGNORE INTO users (username, email, password_hash, role, employee_code, status)
                VALUES ('admin', 'admin@cyberguard.local', ?, 'admin', 'ADMIN001', 'active')
            ''', (admin_password_hash,))
            
            # Create default settings
            default_settings = [
                ('keystroke_interval', '0.01', 'Keystroke logging interval in seconds'),
                ('clipboard_interval', '1.0', 'Clipboard monitoring interval in seconds'),
                ('screen_capture_interval', '60', 'Screen capture interval in seconds'),
                ('mouse_interval', '0.01', 'Mouse logging interval in seconds'),
                ('enable_screen_capture', 'true', 'Enable screen capture feature'),
                ('enable_network_monitor', 'true', 'Enable network monitoring'),
                ('enable_anomaly_detection', 'true', 'Enable ML-based anomaly detection'),
                ('enable_script_detection', 'true', 'Enable script detection'),
                ('encryption_password', 'your-strong-password', 'Database encryption password'),
                ('max_session_duration', '480', 'Maximum session duration in minutes'),
                ('idle_timeout', '30', 'Idle timeout in minutes'),
                ('alert_threshold', '100', 'Keystroke alert threshold per minute'),
                ('sensitive_keywords', 'password,credit,ssn,secret', 'Sensitive keywords for detection')
            ]
            
            for key, value, description in default_settings:
                cursor.execute('''
                    INSERT OR IGNORE INTO settings (setting_key, setting_value, description)
                    VALUES (?, ?, ?)
                ''', (key, value, description))
            
            conn.commit()