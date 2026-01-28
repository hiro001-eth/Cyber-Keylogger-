# CyberKeylogger Pro - CyberGuard Enterprise Security Platform

## Overview
A Flask-based enterprise security monitoring and employee activity tracking dashboard. The web application provides authentication, employee management, and activity monitoring capabilities.

## Project Structure
- `main.py` - Main application entry point, initializes database and Flask server
- `server/webapp/` - Flask web application (routes, templates, static files)
- `server/auth.py` - Authentication manager with JWT tokens
- `database/` - Database models, encryption, and management
- `core/` - Logging services (keylogger, mouse, clipboard) - optional, requires pynput
- `ui/` - GUI components (not used in web mode)

## Running the Application
The application runs on port 5000 with:
```
python main.py
```

## Default Login Credentials
- **Email/Username:** superadmin_@gmail.com
- **Password:** P@$$word123

## Key Features
- User authentication with JWT tokens
- Role-based access (admin/employee)
- Department-based organization
- Dashboard with activity statistics
- Employee management (admin only)
- Alerts monitoring

## Database
Uses SQLite stored in `data/logs.db`. Tables include:
- users, companies, keystrokes, mouse_events, clipboard_events
- screen_captures, alerts, activity_sessions, audit_log, settings

## Environment Notes
- pynput library is not installed (requires kernel headers not available in Replit)
- The web dashboard runs fully without local logging capabilities
- Local logging services are designed for desktop environments

## Recent Changes
- 2026-01-28: Initial setup for Replit environment
- Changed server to bind to 0.0.0.0:5000 for Replit compatibility
- Made pynput imports optional to allow dashboard to run
