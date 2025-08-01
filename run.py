from app import create_app, db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.models.meeting import Meeting
from app.models.notification import Notification
from sqlalchemy import text
import os

app = create_app()

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db, 
        'User': User, 
        'Project': Project, 
        'Task': Task, 
        'Meeting': Meeting,
        'Notification': Notification
    }

def initialize_database():
    """Initialize database tables"""
    try:
        # Force create all tables
        db.create_all()
        print('✅ Database tables created successfully!')
        
        # Verify tables exist
        if 'sqlite' in app.config['SQLALCHEMY_DATABASE_URI']:
            tables = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table';")).fetchall()
            print(f'📋 Available tables: {[table[0] for table in tables]}')
        
    except Exception as e:
        print(f'❌ Database initialization error: {e}')

if __name__ == '__main__':
    with app.app_context():
        initialize_database()
    
    # Get configuration from environment
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    port = int(os.environ.get('PORT', 5000))
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)