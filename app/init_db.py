from app import create_app, db
from app.models.user import User
from app.models.project import Project
from app.models.task import Task
from app.models.meeting import Meeting
from app.models.notification import Notification
from sqlalchemy.exc import SQLAlchemyError

app = create_app()

with app.app_context():
    try:
        db.create_all()
        print("✅ Database tables created successfully during build!")
    except SQLAlchemyError as e:
        print(f"Database initialization error: {e}")

