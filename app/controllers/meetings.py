from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.meeting import Meeting
from app.models.project import Project
from app.models.user import User
from app.forms.meeting_forms import MeetingForm
from app.services.email_service import EmailService
from app.services.notification_service import NotificationService
from datetime import datetime, timedelta

meetings_bp = Blueprint('meetings', __name__, url_prefix='/meetings')

@meetings_bp.route('/project/<int:project_id>/create', methods=['GET', 'POST'])
@login_required
def create_meeting(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Check permissions - only PI can create meetings
    if project.pi_id != current_user.id:
        abort(403)
    
    form = MeetingForm(project=project)
    if form.validate_on_submit():
        # Ensure we have team members to invite
        if not project.team_members:
            flash('Please add team members to the project before scheduling meetings.', 'warning')
            return redirect(url_for('projects.view_project', id=project_id))
        
        meeting = Meeting(
            title=form.title.data,
            agenda=form.agenda.data,
            meeting_date=form.meeting_date.data,
            duration_minutes=form.duration_minutes.data,
            location=form.location.data,
            meeting_link=form.meeting_link.data,
            project_id=project_id,
            created_by_id=current_user.id
        )
        
        # Add attendees
        if form.attendees.data:
            attendees = User.query.filter(User.id.in_(form.attendees.data)).all()
            meeting.attendees = attendees
        
        db.session.add(meeting)
        db.session.commit()
        
        # Send email invitations
        if meeting.attendees:
            EmailService.send_meeting_invitation_email(meeting, meeting.attendees)
            NotificationService.create_meeting_notification(meeting, meeting.attendees)
        
        flash('Meeting scheduled successfully!', 'success')
        return redirect(url_for('projects.view_project', id=project_id))
    
    return render_template('meetings/create.html', form=form, project=project)

@meetings_bp.route('/<int:id>')
@login_required
def view_meeting(id):
    meeting = Meeting.query.get_or_404(id)
    
    # Check permissions
    if (meeting.project.pi_id != current_user.id and 
        current_user not in meeting.attendees):
        abort(403)
    
    return render_template('meetings/view.html', meeting=meeting)

@meetings_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_meeting(id):
    meeting = Meeting.query.get_or_404(id)
    
    # Check permissions - only creator can edit
    if meeting.created_by_id != current_user.id:
        abort(403)
    
    form = MeetingForm(project=meeting.project, obj=meeting)
    if form.validate_on_submit():
        form.populate_obj(meeting)
        
        # Update attendees
        if form.attendees.data:
            attendees = User.query.filter(User.id.in_(form.attendees.data)).all()
            meeting.attendees = attendees
        
        db.session.commit()
        flash('Meeting updated successfully!', 'success')
        return redirect(url_for('meetings.view_meeting', id=meeting.id))
    
    # Pre-select attendees
    form.attendees.data = [attendee.id for attendee in meeting.attendees]
    
    return render_template('meetings/edit.html', form=form, meeting=meeting)

@meetings_bp.route('/calendar')
@login_required
def calendar():
    # Auto-update completed meetings
    completed_meetings = Meeting.query.filter(
        Meeting.meeting_date < datetime.now(),
        Meeting.status == 'scheduled'
    ).all()
    
    for meeting in completed_meetings:
        meeting.status = 'completed'
    
    if completed_meetings:
        db.session.commit()
    
    # Get user's meetings for calendar view
    if current_user.is_pi():
        meetings = Meeting.query.join(Meeting.project)\
                              .filter(Project.pi_id == current_user.id,
                                    Meeting.status.in_(['scheduled', 'completed']))\
                              .order_by(Meeting.meeting_date).all()
    else:
        meetings = Meeting.query.join(Meeting.attendees)\
                              .filter(Meeting.attendees.contains(current_user),
                                    Meeting.status.in_(['scheduled', 'completed']))\
                              .order_by(Meeting.meeting_date).all()
    
    return render_template('meetings/calendar.html', meetings=meetings)

@meetings_bp.route('/<int:id>/cancel', methods=['POST'])
@login_required
def cancel_meeting(id):
    meeting = Meeting.query.get_or_404(id)
    
    # Check permissions - only creator can cancel
    if meeting.created_by_id != current_user.id:
        abort(403)
    
    meeting.status = 'cancelled'
    db.session.commit()
    
    flash('Meeting cancelled successfully!', 'success')
    return redirect(url_for('meetings.calendar'))