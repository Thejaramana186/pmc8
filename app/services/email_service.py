from flask import current_app, render_template
from flask_mail import Message
from app import mail
from datetime import datetime

class EmailService:
    @staticmethod
    def send_email(subject, recipients, html_body, text_body=None):
        """Send email with HTML and optional text body"""
        if not current_app.config.get('MAIL_USERNAME'):
            current_app.logger.warning("Email not configured - MAIL_USERNAME not set. Please configure email settings in .env file.")
            return False
            
        try:
            msg = Message(
                subject=subject,
                recipients=recipients,
                html=html_body,
                body=text_body
            )
            mail.send(msg)
            current_app.logger.info(f"✅ Email sent successfully to {recipients} via {current_app.config.get('MAIL_SERVER')}")
            return True
        except Exception as e:
            current_app.logger.error(f"❌ Email send failed to {recipients}: {str(e)}")
            current_app.logger.error(f"📧 Email settings: Server={current_app.config.get('MAIL_SERVER')}, Port={current_app.config.get('MAIL_PORT')}, TLS={current_app.config.get('MAIL_USE_TLS')}, SSL={current_app.config.get('MAIL_USE_SSL')}")
            return False
    
    @staticmethod
    def send_task_assignment_email(task, assignee):
        """Send email notification for task assignment"""
        subject = f"New Task Assigned: {task.title}"
        
        html_body = render_template('emails/task_assignment.html', 
                                  task=task, assignee=assignee)
        
        return EmailService.send_email(
            subject=subject,
            recipients=[assignee.email],
            html_body=html_body
        )
    
    @staticmethod
    def send_meeting_invitation_email(meeting, attendees):
        """Send email invitation for meeting"""
        subject = f"Meeting Invitation: {meeting.title}"
        
        html_body = render_template('emails/meeting_invitation.html', 
                                  meeting=meeting, attendees=attendees)
        
        recipient_emails = [attendee.email for attendee in attendees]
        
        return EmailService.send_email(
            subject=subject,
            recipients=recipient_emails,
            html_body=html_body
        )
    
    @staticmethod
    def send_meeting_reminder_email(meeting, attendees):
        """Send meeting reminder email (24 hours before)"""
        subject = f"Meeting Reminder: {meeting.title}"
        
        html_body = render_template('emails/meeting_reminder.html', 
                                  meeting=meeting, attendees=attendees)
        
        recipient_emails = [attendee.email for attendee in attendees]
        
        return EmailService.send_email(
            subject=subject,
            recipients=recipient_emails,
            html_body=html_body
        )
    
    @staticmethod
    def send_project_assignment_email(project, team_members):
        """Send email notification for project assignment"""
        subject = f"You've been assigned to project: {project.title}"
        
        html_body = render_template('emails/project_assignment.html', 
                                  project=project, team_members=team_members)
        
        recipient_emails = [member.email for member in team_members]
        
        return EmailService.send_email(
            subject=subject,
            recipients=recipient_emails,
            html_body=html_body
        )