from wtforms import StringField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Length
from flask_wtf import FlaskForm

class CreateListForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=50, message="Title length must be between 3 and 50 syllables")])
    description = StringField('Description')
    submit = SubmitField('Create')

class CreateTaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    done = BooleanField('Completed')
    submit = SubmitField('Add')