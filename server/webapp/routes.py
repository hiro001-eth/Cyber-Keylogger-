from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from server.auth import AuthManager, login_required, admin_required
import sqlite3
from datetime import datetime

webapp_routes = Blueprint('webapp_routes', __name__)
auth_manager = AuthManager('data/logs.db')

@webapp_routes.route('/')
def home():
    return redirect(url_for('webapp_routes.login'))

@webapp_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        result = auth_manager.login_user(username, password)
        
        if result['success']:
            session['user_token'] = result['token']
            session['user'] = result['user']
            flash('Login successful!', 'success')
            return redirect(url_for('webapp_routes.dashboard'))
        else:
            flash(result['message'], 'error')

    return render_template('login_cg.html')

@webapp_routes.route('/dashboard')
@login_required
def dashboard():
    user = auth_manager.get_user_by_token(session['user_token'])
    if not user:
        session.clear()
        return redirect(url_for('webapp_routes.login'))

    return render_template('dashboard_cg.html', user=user)

@webapp_routes.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully', 'success')
    return redirect(url_for('webapp_routes.login'))

@webapp_routes.route('/api/employees', methods=['GET', 'POST'])
@login_required
def employees_api():
    user = auth_manager.get_user_by_token(session['user_token'])
    if not user or user['role'] != 'admin':
        return jsonify({'success': False, 'message': 'Admin access required'}), 403
    
    if request.method == 'POST':
        employee_data = request.json
        result = auth_manager.create_employee(user['id'], employee_data)
        return jsonify(result)
    
    # GET - return list of employees
    with sqlite3.connect('data/logs.db') as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT id, username, email, role, employee_code, department, position, status, created_at
            FROM users WHERE role = 'employee' ORDER BY created_at DESC
        ''')
        employees = cursor.fetchall()
        
        employee_list = []
        for emp in employees:
            employee_list.append({
                'id': emp[0],
                'username': emp[1],
                'email': emp[2],
                'role': emp[3],
                'employee_code': emp[4],
                'department': emp[5],
                'position': emp[6],
                'status': emp[7],
                'created_at': emp[8]
            })
        
        return jsonify({'success': True, 'employees': employee_list})

@webapp_routes.route('/api/stats')
@login_required
def stats_api():
    user = auth_manager.get_user_by_token(session['user_token'])
    if not user:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    with sqlite3.connect('data/logs.db') as conn:
        cursor = conn.cursor()
        
        # Get basic stats
        cursor.execute('SELECT COUNT(*) FROM users WHERE role = "employee" AND status = "active"')
        active_employees = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM keystrokes WHERE DATE(timestamp) = DATE("now")')
        today_keystrokes = cursor.fetchone()[0]
        
        cursor.execute('SELECT COUNT(*) FROM alerts WHERE is_resolved = 0')
        active_alerts = cursor.fetchone()[0]
        
        # Get user-specific stats if employee
        if user['role'] == 'employee':
            cursor.execute('''
                SELECT COUNT(*) FROM keystrokes 
                WHERE user_id = ? AND DATE(timestamp) = DATE("now")
            ''', (user['id'],))
            user_keystrokes = cursor.fetchone()[0]
        else:
            user_keystrokes = 0
        
        return jsonify({
            'success': True,
            'stats': {
                'active_employees': active_employees,
                'today_keystrokes': today_keystrokes,
                'active_alerts': active_alerts,
                'user_keystrokes': user_keystrokes
            }
        })

@webapp_routes.route('/api/alerts')
@login_required
def alerts_api():
    user = auth_manager.get_user_by_token(session['user_token'])
    if not user:
        return jsonify({'success': False, 'message': 'Authentication required'}), 401
    
    with sqlite3.connect('data/logs.db') as conn:
        cursor = conn.cursor()
        
        if user['role'] == 'admin':
            cursor.execute('''
                SELECT a.id, a.alert_type, a.severity, a.message, a.timestamp, u.username
                FROM alerts a
                JOIN users u ON a.user_id = u.id
                WHERE a.is_resolved = 0
                ORDER BY a.timestamp DESC
                LIMIT 10
            ''')
        else:
            cursor.execute('''
                SELECT id, alert_type, severity, message, timestamp
                FROM alerts
                WHERE user_id = ? AND is_resolved = 0
                ORDER BY timestamp DESC
                LIMIT 10
            ''', (user['id'],))
        
        alerts = cursor.fetchall()
        alert_list = []
        
        for alert in alerts:
            if user['role'] == 'admin':
                alert_list.append({
                    'id': alert[0],
                    'type': alert[1],
                    'severity': alert[2],
                    'message': alert[3],
                    'timestamp': alert[4],
                    'username': alert[5]
                })
            else:
                alert_list.append({
                    'id': alert[0],
                    'type': alert[1],
                    'severity': alert[2],
                    'message': alert[3],
                    'timestamp': alert[4]
                })
        
        return jsonify({'success': True, 'alerts': alert_list})

@webapp_routes.route('/alerts')
@login_required
def alerts():
    user = auth_manager.get_user_by_token(session['user_token'])
    if not user:
        return redirect(url_for('webapp_routes.login'))
    return render_template('alerts.html', user=user)

@webapp_routes.route('/reports')
@login_required
def reports():
    user = auth_manager.get_user_by_token(session['user_token'])
    if not user:
        return redirect(url_for('webapp_routes.login'))
    return render_template('reports.html', user=user)

@webapp_routes.route('/settings')
@login_required
def settings():
    user = auth_manager.get_user_by_token(session['user_token'])
    if not user:
        return redirect(url_for('webapp_routes.login'))
    return render_template('settings.html', user=user)