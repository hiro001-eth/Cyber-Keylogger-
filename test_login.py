#!/usr/bin/env python3

import sqlite3
from server.auth import AuthManager

def test_admin_login():
    """Test the admin login functionality"""
    print("🔍 Testing admin login...")
    
    # Initialize auth manager
    auth_manager = AuthManager('data/logs.db')
    
    # Test login with admin/admin
    result = auth_manager.login_user('admin', 'admin')
    
    print(f"Login result: {result}")
    
    if result['success']:
        print("✅ Admin login successful!")
        print(f"User data: {result['user']}")
    else:
        print("❌ Admin login failed!")
        print(f"Error: {result['message']}")
    
    # Check database directly
    with sqlite3.connect('data/logs.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT username, password_hash, role FROM users WHERE username = "admin"')
        user = cursor.fetchone()
        
        if user:
            print(f"✅ Admin user found in database")
            print(f"Username: {user[0]}")
            print(f"Role: {user[2]}")
            print(f"Password hash: {user[1][:50]}...")
        else:
            print("❌ Admin user not found in database")

if __name__ == "__main__":
    test_admin_login() 