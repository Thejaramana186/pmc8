from datetime import datetime
from app import db

# Association table for many-to-many relationship between meetings and attendees
meeting_attendees = db.Table('meeting_attendees',
    db.Column('meeting_id', db.Integer, db.ForeignKey('meeting.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class Meeting(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    agenda = db.Column(db.Text)
    meeting_date = db.Column(db.DateTime, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    location = db.Column(db.String(200))
    meeting_link = db.Column(db.String(500))  # For virtual meetings
    status = db.Column(db.String(20), nullable=False, default='scheduled')  # scheduled, completed, cancelled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Foreign keys
    project_id = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    creator = db.relationship('User', backref='created_meetings')
    attendees = db.relationship('User', secondary=meeting_attendees, lazy='subquery',
                              backref=db.backref('meetings_attending', lazy=True))
    
    def get_status_color(self):
        status_colors = {
            'scheduled': 'primary',
            'completed': 'success',
            'cancelled': 'danger'
        }
        return status_colors.get(self.status, 'secondary')
    
    def __repr__(self):
        return f'<Meeting {self.title}>'