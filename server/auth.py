import hashlib
import secrets
import sqlite3
from datetime import datetime, timedelta
from functools import wraps
from flask import session, redirect, url_for, flash, request
import jwt
import os

class AuthManager:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.secret_key = os.environ.get('SECRET_KEY', 'your-super-secret-key-change-in-production')
    
    def hash_password(self, password: str) -> str:
        """Hash password using PBKDF2"""
        salt = secrets.token_hex(16)
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 600000)
        return f"pbkdf2:sha256:600000${salt}${hash_obj.hex()}"
    
    def verify_password(self, password: str, password_hash: str) -> bool:
        """Verify password against hash"""
        try:
            parts = password_hash.split('$')
            if len(parts) != 3:
                print(f"Invalid password hash format: {password_hash}")
                return False
            
            algorithm, salt, hash_hex = parts
            if algorithm != 'pbkdf2:sha256:600000':
                print(f"Unsupported algorithm: {algorithm}")
                return False
            
            hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 600000)
            result = hash_obj.hex() == hash_hex
            print(f"Password verification: {result}")
            return result
        except Exception as e:
            print(f"Password verification error: {e}")
            return False
    
    def login_user(self, identifier, password, company_id=None) -> dict:
        """Authenticate user and return user data"""
        print(f"Login attempt for identifier: {identifier}, company: {company_id}")
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            if company_id:
                cursor.execute('''
                    SELECT id, username, email, password_hash, role, employee_code, 
                           company_id, department, position, status
                    FROM users 
                    WHERE (username = ? OR email = ?) 
                      AND company_id = ? 
                      AND status = 'active'
                ''', (identifier, identifier, company_id))
            else:
                cursor.execute('''
                    SELECT id, username, email, password_hash, role, employee_code, 
                           company_id, department, position, status
                    FROM users 
                    WHERE (username = ? OR email = ?) 
                      AND status = 'active'
                ''', (identifier, identifier))
            
            user = cursor.fetchone()
            print(f"User found: {user is not None}")
            
            if user:
                print(f"Stored password hash: {user[3]}")
                if self.verify_password(password, user[3]):
                    print("Password verified successfully")
                    # Update last login
                    cursor.execute('''
                        UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?
                    ''', (user[0],))
                    
                    user_data = {
                        'id': user[0],
                        'username': user[1],
                        'email': user[2],
                        'role': user[4],
                        'employee_code': user[5],
                        'company_id': user[6],
                        'department': user[7],
                        'position': user[8],
                        'status': user[9]
                    }
                    
                    # Create session token
                    token = jwt.encode({
                        'user_id': user[0],
                        'username': user[1],
                        'role': user[4],
                        'exp': datetime.utcnow() + timedelta(hours=8)
                    }, self.secret_key, algorithm='HS256')
                    
                    print("Login successful")
                    return {'success': True, 'user': user_data, 'token': token}
                else:
                    print("Password verification failed")
            else:
                print("User not found")
            
            return {'success': False, 'message': 'Invalid credentials'}
    
    def create_employee(self, admin_id: int, employee_data: dict) -> dict:
        """Create new employee account"""
        try:
            # Generate employee code
            employee_code = self._generate_employee_code()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Check if username/email already exists
                cursor.execute('''
                    SELECT id FROM users WHERE username = ? OR email = ?
                ''', (employee_data['username'], employee_data['email']))
                
                if cursor.fetchone():
                    return {'success': False, 'message': 'Username or email already exists'}
                
                # Create employee
                password_hash = self.hash_password(employee_data['password'])
                
                cursor.execute('''
                    INSERT INTO users (username, email, password_hash, role, employee_code,
                                    company_id, department, position, created_by)
                    VALUES (?, ?, ?, 'employee', ?, ?, ?, ?, ?)
                ''', (
                    employee_data['username'],
                    employee_data['email'],
                    password_hash,
                    employee_code,
                    employee_data.get('company_id'),
                    employee_data.get('department'),
                    employee_data.get('position'),
                    admin_id
                ))
                
                employee_id = cursor.lastrowid
                
                # Log audit
                cursor.execute('''
                    INSERT INTO audit_log (admin_id, action_type, target_user_id, details)
                    VALUES (?, 'create_employee', ?, ?)
                ''', (admin_id, employee_id, f"Created employee: {employee_data['username']}"))
                
                return {
                    'success': True,
                    'employee_code': employee_code,
                    'message': f'Employee created successfully. Code: {employee_code}'
                }
                
        except Exception as e:
            return {'success': False, 'message': f'Error creating employee: {str(e)}'}
    
    def _generate_employee_code(self) -> str:
        """Generate unique employee code"""
        import random
        import string
        
        while True:
            code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('SELECT id FROM users WHERE employee_code = ?', (code,))
                if not cursor.fetchone():
                    return code
    
    def get_user_by_token(self, token: str) -> dict:
        """Get user data from JWT token"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT id, username, email, role, employee_code, company_id, 
                           department, position, status
                    FROM users WHERE id = ? AND status = 'active'
                ''', (payload['user_id'],))
                
                user = cursor.fetchone()
                if user:
                    return {
                        'id': user[0],
                        'username': user[1],
                        'email': user[2],
                        'role': user[3],
                        'employee_code': user[4],
                        'company_id': user[5],
                        'department': user[6],
                        'position': user[7],
                        'status': user[8]
                    }
        except:
            pass
        return None

# Flask decorators for authentication
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_token' not in session:
            return redirect(url_for('webapp_routes.login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_token' not in session:
            return redirect(url_for('webapp_routes.login'))
        
        auth_manager = AuthManager('data/logs.db')
        user = auth_manager.get_user_by_token(session['user_token'])
        
        if not user or user['role'] != 'admin':
            flash('Admin access required', 'error')
            return redirect(url_for('webapp_routes.dashboard'))
        
        return f(*args, **kwargs)
    return decorated_function 