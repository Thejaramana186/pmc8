from app import db
from app.models.notification import Notification

class NotificationService:
    @staticmethod
    def create_notification(user_id, title, message, notification_type, 
                          project_id=None, task_id=None, meeting_id=None):
        """Create a new notification"""
        notification = Notification(
            user_id=user_id,
            title=title,
            message=message,
            notification_type=notification_type,
            project_id=project_id,
            task_id=task_id,
            meeting_id=meeting_id
        )
        db.session.add(notification)
        db.session.commit()
        return notification
    
    @staticmethod
    def create_task_assignment_notification(task):
        """Create notification for task assignment"""
        if task.assigned_to_id:
            return NotificationService.create_notification(
                user_id=task.assigned_to_id,
                title=f"New Task Assigned: {task.title}",
                message=f"You have been assigned a new task in project '{task.project.title}'",
                notification_type='task_assigned',
                project_id=task.project_id,
                task_id=task.id
            )
    
    @staticmethod
    def create_meeting_notification(meeting, attendees):
        """Create notifications for meeting attendees"""
        notifications = []
        for attendee in attendees:
            notification = NotificationService.create_notification(
                user_id=attendee.id,
                title=f"Meeting Scheduled: {meeting.title}",
                message=f"You have been invited to a meeting for project '{meeting.project.title}'",
                notification_type='meeting_scheduled',
                project_id=meeting.project_id,
                meeting_id=meeting.id
            )
            notifications.append(notification)
        return notifications
    
    @staticmethod
    def create_project_assignment_notifications(project, team_members):
        """Create notifications for project assignment"""
        notifications = []
        for member in team_members:
            notification = NotificationService.create_notification(
                user_id=member.id,
                title=f"Assigned to Project: {project.title}",
                message=f"You have been assigned to work on project '{project.title}' by {project.owner.get_full_name()}",
                notification_type='project_assigned',
                project_id=project.id
            )
            notifications.append(notification)
        return notifications
    
    @staticmethod
    def mark_as_read(notification_id, user_id):
        """Mark notification as read"""
        notification = Notification.query.filter_by(id=notification_id, user_id=user_id).first()
        if notification:
            notification.is_read = True
            db.session.commit()
            return True
        return False