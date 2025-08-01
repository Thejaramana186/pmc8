from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from datetime import datetime, date
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    
    from app.models.user import User
    
    # Add datetime to Jinja2 globals
    @app.context_processor
    def inject_datetime():
        return {
            'datetime': datetime,
            'date': date,
            'now': datetime.now()
        }
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from app.controllers.auth import auth_bp
    from app.controllers.main import main_bp
    from app.controllers.projects import projects_bp
    from app.controllers.tasks import tasks_bp
    from app.controllers.meetings import meetings_bp
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(projects_bp)
    app.register_blueprint(tasks_bp)
    app.register_blueprint(meetings_bp)
    
    return app