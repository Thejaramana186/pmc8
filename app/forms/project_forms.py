from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateField, SelectField, FloatField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError
from app.models.project import Project
from app.models.user import User

class ProjectForm(FlaskForm):
    title = StringField('Project Title', validators=[DataRequired(), Length(max=200)])
    project_id = StringField('Project ID', validators=[DataRequired(), Length(max=50)])
    description = TextAreaField('Description')
    start_date = DateField('Start Date', validators=[DataRequired()])
    end_date = DateField('End Date', validators=[DataRequired()])
    status = SelectField('Status', choices=[
        ('proposal', 'Proposal'),
        ('active', 'Active'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed')
    ], validators=[DataRequired()])
    funding_source = StringField('Funding Source', validators=[Length(max=200)])
    funding_amount = FloatField('Funding Amount', validators=[NumberRange(min=0)])
    team_members = SelectMultipleField('Team Members', coerce=int)
    submit = SubmitField('Save Project')
    
    def __init__(self, original_project=None, *args, **kwargs):
        super(ProjectForm, self).__init__(*args, **kwargs)
        self.original_project = original_project
        # Populate team members choices
        self.team_members.choices = [(user.id, f"{user.get_full_name()} ({user.username})") 
                                   for user in User.query.filter_by(role='team_member').all()]
    
    def validate_project_id(self, project_id):
        project = Project.query.filter_by(project_id=project_id.data).first()
        if project and (self.original_project is None or project.id != self.original_project.id):
            raise ValidationError('Project ID already exists. Please choose a different one.')
    
    def validate_end_date(self, end_date):
        if self.start_date.data and end_date.data < self.start_date.data:
            raise ValidationError('End date cannot be before start date.')