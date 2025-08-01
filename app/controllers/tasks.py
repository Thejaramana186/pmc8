from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.task import Task, TaskComment
from app.models.project import Project
from app.forms.task_forms import TaskForm, TaskStatusForm
from app.services.email_service import EmailService
from app.services.notification_service import NotificationService
from datetime import datetime

tasks_bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@tasks_bp.route('/project/<int:project_id>/create', methods=['GET', 'POST'])
@login_required
def create_task(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Check permissions
    if not current_user.is_pi() and current_user not in project.team_members:
        abort(403)
    
    form = TaskForm(project=project)
    if form.validate_on_submit():
        # Ensure we have team members to assign to
        if not project.team_members:
            flash('Please add team members to the project before creating tasks.', 'warning')
            return redirect(url_for('projects.view_project', id=project_id))
        
        task = Task(
            title=form.title.data,
            description=form.description.data,
            assigned_to_id=form.assigned_to.data,
            priority=form.priority.data,
            due_date=form.due_date.data,
            project_id=project_id,
            created_by_id=current_user.id
        )
        
        db.session.add(task)
        db.session.commit()
        
        # Send email notification to assignee
        if task.assignee:
            EmailService.send_task_assignment_email(task, task.assignee)
            NotificationService.create_task_assignment_notification(task)
        
        flash('Task created successfully!', 'success')
        return redirect(url_for('projects.view_project', id=project_id))
    
    return render_template('tasks/create.html', form=form, project=project)

@tasks_bp.route('/<int:id>')
@login_required
def view_task(id):
    task = Task.query.get_or_404(id)
    
    # Check permissions
    if (not current_user.is_pi() and 
        current_user not in task.project.team_members and 
        task.assigned_to_id != current_user.id):
        abort(403)
    
    return render_template('tasks/view.html', task=task)

@tasks_bp.route('/<int:id>/update-status', methods=['GET', 'POST'])
@login_required
def update_task_status(id):
    task = Task.query.get_or_404(id)
    
    # Check permissions - only assignee or PI can update status
    if (task.assigned_to_id != current_user.id and 
        task.project.pi_id != current_user.id):
        abort(403)
    
    form = TaskStatusForm()
    if form.validate_on_submit():
        old_status = task.status
        task.status = form.status.data
        
        if form.status.data == 'completed' and old_status != 'completed':
            task.completed_at = datetime.utcnow()
        
        db.session.commit()
        
        # Add comment if provided
        if form.comment.data:
            comment = TaskComment(
                content=form.comment.data,
                task_id=task.id,
                user_id=current_user.id
            )
            db.session.add(comment)
            db.session.commit()
        
        flash('Task status updated successfully!', 'success')
        return redirect(url_for('tasks.view_task', id=task.id))
    
    form.status.data = task.status
    return render_template('tasks/update_status.html', form=form, task=task)

@tasks_bp.route('/<int:id>/comment', methods=['POST'])
@login_required
def add_comment(id):
    task = Task.query.get_or_404(id)
    
    # Check permissions
    if (not current_user.is_pi() and 
        current_user not in task.project.team_members and 
        task.assigned_to_id != current_user.id):
        abort(403)
    
    content = request.form.get('content')
    if content:
        comment = TaskComment(
            content=content,
            task_id=task.id,
            user_id=current_user.id
        )
        db.session.add(comment)
        db.session.commit()
        flash('Comment added successfully!', 'success')
    
    return redirect(url_for('tasks.view_task', id=task.id))

@tasks_bp.route('/my-tasks')
@login_required
def my_tasks():
    if current_user.is_pi():
        # PI sees all tasks from their projects
        tasks = Task.query.join(Task.project).filter_by(pi_id=current_user.id)\
                         .order_by(Task.due_date.asc()).all()
    else:
        # Team members see only their assigned tasks
        tasks = Task.query.filter_by(assigned_to_id=current_user.id)\
                         .order_by(Task.due_date.asc()).all()
    
    return render_template('tasks/my_tasks.html', tasks=tasks)