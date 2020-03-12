from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class CreatePostForm(FlaskForm): 
    title = StringField('Title', validators=[DataRequired(), Length(max=50)])
    text = StringField('Text', validators=[DataRequired()])
    create = SubmitField('Create')
