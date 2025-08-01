from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models.project import Project
from app.models.user import User
from app.forms.project_forms import ProjectForm
from app.utils.helpers import get_user_projects
from app.services.email_service import EmailService
from app.services.notification_service import NotificationService

projects_bp = Blueprint('projects', __name__, url_prefix='/projects')

@projects_bp.route('/')
@login_required
def list_projects():
    projects = get_user_projects(current_user)
    return render_template('projects/list.html', projects=projects)

@projects_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_project():
    if not current_user.is_pi():
        abort(403)
    
    form = ProjectForm()
    if form.validate_on_submit():
        project = Project(
            title=form.title.data,
            project_id=form.project_id.data,
            description=form.description.data,
            start_date=form.start_date.data,
            end_date=form.end_date.data,
            status=form.status.data,
            funding_source=form.funding_source.data,
            funding_amount=form.funding_amount.data,
            pi_id=current_user.id
        )
        
        db.session.add(project)
        db.session.flush()  # Get the project ID
        
        # Add team members
        if form.team_members.data:
            team_members = User.query.filter(User.id.in_(form.team_members.data)).all()
            project.team_members = team_members
        
        db.session.commit()
        flash('Project created successfully!', 'success')
        
        # Send welcome emails to team members
        if project.team_members:
            EmailService.send_project_assignment_email(project, project.team_members)
            NotificationService.create_project_assignment_notifications(project, project.team_members)
        
        return redirect(url_for('projects.view_project', id=project.id))
    
    return render_template('projects/create.html', form=form)

@projects_bp.route('/<int:id>')
@login_required
def view_project(id):
    project = Project.query.get_or_404(id)
    
    # Check access permissions
    if not current_user.is_pi() and current_user not in project.team_members:
        abort(403)
    
    return render_template('projects/view.html', project=project)

@projects_bp.route('/<int:id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(id):
    project = Project.query.get_or_404(id)
    
    # Only PI can edit project
    if project.pi_id != current_user.id:
        abort(403)
    
    form = ProjectForm(original_project=project, obj=project)
    if form.validate_on_submit():
        # Manually populate fields to handle relationships properly
        project.title = form.title.data
        project.project_id = form.project_id.data
        project.description = form.description.data
        project.start_date = form.start_date.data
        project.end_date = form.end_date.data
        project.status = form.status.data
        project.funding_source = form.funding_source.data
        project.funding_amount = form.funding_amount.data
        
        # Update team members
        if form.team_members.data:
            team_members = User.query.filter(User.id.in_(form.team_members.data)).all()
            project.team_members = team_members
        else:
            project.team_members = []
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        
        # Send emails to newly added team members
        if project.team_members:
            EmailService.send_project_assignment_email(project, project.team_members)
            NotificationService.create_project_assignment_notifications(project, project.team_members)
        
        return redirect(url_for('projects.view_project', id=project.id))
    
    # Pre-select team members
    form.team_members.data = [member.id for member in project.team_members]
    
    return render_template('projects/edit.html', form=form, project=project)

@projects_bp.route('/<int:id>/delete', methods=['POST'])
@login_required
def delete_project(id):
    project = Project.query.get_or_404(id)
    
    # Only PI can delete project
    if project.pi_id != current_user.id:
        abort(403)
    
    db.session.delete(project)
    db.session.commit()
    flash('Project deleted successfully!', 'success')
    return redirect(url_for('projects.list_projects'))