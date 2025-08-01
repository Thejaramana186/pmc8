from datetime import datetime
from app import db

class Notification(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), nullable=False)  # task_assigned, meeting_scheduled, etc.
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'))
    task_id = db.Column(db.Integer, db.ForeignKey('task.id'))
    meeting_id = db.Column(db.Integer, db.ForeignKey('meeting.id'))
    
    # Relationships
    user = db.relationship('User', backref='notifications')
    project = db.relationship('Project', backref='notifications')
    task = db.relationship('Task', backref='notifications')
    meeting = db.relationship('Meeting', backref='notifications')
    
    def __repr__(self):
        return f'<Notification {self.title}>'