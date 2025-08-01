from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length
from app.models.user import User

class TaskForm(FlaskForm):
    title = StringField('Task Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description')
    assigned_to = SelectField('Assign To', coerce=int, validators=[DataRequired()])
    priority = SelectField('Priority', choices=[
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High')
    ], validators=[DataRequired()])
    due_date = DateField('Due Date')
    submit = SubmitField('Create Task')
    
    def __init__(self, project=None, *args, **kwargs):
        super(TaskForm, self).__init__(*args, **kwargs)
        if project:
            # Only include team members of the project, not the PI
            choices = [(member.id, member.get_full_name()) for member in project.team_members]
            self.assigned_to.choices = choices

class TaskStatusForm(FlaskForm):
    status = SelectField('Status', choices=[
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed')
    ], validators=[DataRequired()])
    comment = TextAreaField('Add Comment')
    submit = SubmitField('Update Status')