from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app import db
from app.models.project import Project
from app.models.task import Task
from app.models.meeting import Meeting
from app.models.notification import Notification
from app.utils.helpers import get_user_projects, calculate_project_stats, get_recent_activities
from datetime import datetime, timedelta

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/dashboard')
@login_required
def dashboard():
    # Get user's projects
    projects = get_user_projects(current_user)
    
    # Calculate statistics
    stats = calculate_project_stats(projects)
    
    # Get upcoming meetings (next 7 days)
    upcoming_meetings = []
    if current_user.is_pi():
        upcoming_meetings = Meeting.query.join(Meeting.project)\
                                       .filter(Meeting.meeting_date >= datetime.now(),
                                              Meeting.meeting_date <= datetime.now() + timedelta(days=7),
                                              Project.pi_id == current_user.id,
                                              Meeting.status == 'scheduled')\
                                       .order_by(Meeting.meeting_date).limit(5).all()
    else:
        upcoming_meetings = Meeting.query.filter(Meeting.attendees.any(id=current_user.id))\
                                       .filter(Meeting.meeting_date >= datetime.now(),
                                              Meeting.meeting_date <= datetime.now() + timedelta(days=7),
                                              Meeting.status == 'scheduled')\
                                       .order_by(Meeting.meeting_date).limit(5).all()
    
    # Auto-update completed meetings
    completed_meetings = Meeting.query.filter(
        Meeting.meeting_date < datetime.now(),
        Meeting.status == 'scheduled'
    ).all()
    
    for meeting in completed_meetings:
        meeting.status = 'completed'
    
    if completed_meetings:
        db.session.commit()
    
    # Get pending tasks
    pending_tasks = []
    if current_user.is_pi():
        pending_tasks = Task.query.join(Task.project)\
                                .filter(Task.status.in_(['todo', 'in_progress']),
                                       Project.pi_id == current_user.id)\
                                .order_by(Task.due_date).limit(10).all()
    else:
        pending_tasks = Task.query.filter(Task.assigned_to_id == current_user.id,
                                        Task.status.in_(['todo', 'in_progress']))\
                                .order_by(Task.due_date).limit(10).all()
    
    # Get recent notifications
    recent_notifications = Notification.query.filter_by(user_id=current_user.id, is_read=False)\
                                           .order_by(Notification.created_at.desc()).limit(5).all()
    
    # Get recent activities
    recent_activities = get_recent_activities(current_user, 10)
    
    return render_template('main/dashboard.html',
                         projects=projects,
                         stats=stats,
                         upcoming_meetings=upcoming_meetings,
                         pending_tasks=pending_tasks,
                         recent_notifications=recent_notifications,
                         recent_activities=recent_activities)

@main_bp.route('/profile')
@login_required
def profile():
    return render_template('main/profile.html')