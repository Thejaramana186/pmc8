from datetime import datetime
from app import db

# Association table for many-to-many relationship between projects and team members
project_members = db.Table('project_members',
    db.Column('project_id', db.Integer, db.ForeignKey('project.id'), primary_key=True),
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True)
)

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    project_id = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False, default='proposal')  # proposal, active, on_hold, completed
    funding_source = db.Column(db.String(200))
    funding_amount = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign keys
    pi_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    tasks = db.relationship('Task', backref='project', lazy=True, cascade='all, delete-orphan')
    meetings = db.relationship('Meeting', backref='project', lazy=True, cascade='all, delete-orphan')
    team_members = db.relationship('User', secondary=project_members, lazy='subquery',
                                 backref=db.backref('assigned_projects', lazy=True))
    
    def get_progress_percentage(self):
        total_tasks = len(self.tasks)
        if total_tasks == 0:
            return 0
        completed_tasks = len([task for task in self.tasks if task.status == 'completed'])
        return round((completed_tasks / total_tasks) * 100, 1)
    
    def get_status_color(self):
        status_colors = {
            'proposal': 'warning',
            'active': 'success',
            'on_hold': 'secondary',
            'completed': 'primary'
        }
        return status_colors.get(self.status, 'secondary')
    
    def __repr__(self):
        return f'<Project {self.title}>'