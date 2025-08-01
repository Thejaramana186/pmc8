from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, DateTimeField, IntegerField, SelectMultipleField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, Optional

class MeetingForm(FlaskForm):
    title = StringField('Meeting Title', validators=[DataRequired(), Length(max=200)])
    agenda = TextAreaField('Agenda')
    meeting_date = DateTimeField('Meeting Date & Time', validators=[DataRequired()], 
                                format='%Y-%m-%d %H:%M')
    duration_minutes = IntegerField('Duration (minutes)', validators=[NumberRange(min=15, max=480)], 
                                  default=60)
    location = StringField('Location (Optional)', validators=[Optional(), Length(max=200)])
    meeting_link = StringField('Meeting Link (for virtual meetings)', validators=[Length(max=500)])
    attendees = SelectMultipleField('Attendees', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Schedule Meeting')
    
    def __init__(self, project=None, *args, **kwargs):
        super(MeetingForm, self).__init__(*args, **kwargs)
        if project:
            # Only include team members of the project for meeting attendees
            choices = [(member.id, member.get_full_name()) for member in project.team_members]
            self.attendees.choices = choices