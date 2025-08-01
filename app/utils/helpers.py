from datetime import datetime, timedelta
from flask_login import current_user

def format_date(date):
    """Format date for display"""
    if date:
        return date.strftime('%B %d, %Y')
    return ''

def format_datetime(datetime_obj):
    """Format datetime for display"""
    if datetime_obj:
        return datetime_obj.strftime('%B %d, %Y at %I:%M %p')
    return ''

def is_upcoming_deadline(due_date, days=7):
    """Check if deadline is within specified days"""
    if due_date:
        return due_date <= (datetime.now().date() + timedelta(days=days))
    return False

def get_user_projects(user):
    """Get projects accessible to user based on role"""
    if user.is_pi():
        return user.owned_projects
    else:
        return user.assigned_projects

def calculate_project_stats(projects):
    """Calculate statistics for projects"""
    total_projects = len(projects)
    active_projects = len([p for p in projects if p.status == 'active'])
    completed_projects = len([p for p in projects if p.status == 'completed'])
    total_funding = sum([p.funding_amount or 0 for p in projects])
    
    return {
        'total_projects': total_projects,
        'active_projects': active_projects,  
        'completed_projects': completed_projects,
        'total_funding': total_funding
    }

def get_recent_activities(user, limit=10):
    """Get recent activities for user"""
    activities = []
    
    # Get recent tasks
    if user.is_pi():
        from app.models.task import Task
        recent_tasks = Task.query.join(Task.project).filter_by(pi_id=user.id)\
                          .order_by(Task.updated_at.desc()).limit(limit).all()
    else:
        recent_tasks = user.assigned_tasks[-limit:]
    
    for task in recent_tasks:
        activities.append({
            'type': 'task',
            'title': f"Task '{task.title}' updated",
            'project': task.project.title,
            'date': task.updated_at,
            'status': task.status
        })
    
    # Sort by date
    activities.sort(key=lambda x: x['date'], reverse=True)
    return activities[:limit]