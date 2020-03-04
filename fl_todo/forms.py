from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from .models import User
from flask_login import current_user

class UserRegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=16)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirmed = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6, max=30), EqualTo('password', message='The passwords are not the same')])
    submit = SubmitField('Submit')

    def validate_username(self, username):
        if User.query.filter_by(username=username.data).first():
            raise ValidationError("That username is already taken")

    def validate_email(self, email):
        if User.query.filter_by(email=email.data).first():
            raise ValidationError("That email is already taken")

class UserLoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField('Submit')

# ========================= > Reset Password Area

class UserEmailForResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Sumbit')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None: 
            raise ValidationError('That user wasn\'t found')

class UserPasswordResetForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6, max=30)])
    confirmed = PasswordField('Confirm Password', validators=[DataRequired(), Length(min=6, max=30), EqualTo('password', message='The passwords are not the same')])
    submit = SubmitField('Sumbit')

# ========================= > Reset Password Area

class UserAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=16)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    avatar = FileField('Change Avatar', validators=[FileAllowed(['png', 'jpeg', 'jpg'], message="That format is not supported")])
    submit = SubmitField('Update')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user and current_user.email != user.email: 
            raise ValidationError('That email is already taken')
        
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user and current_user.username != user.username: 
            raise ValidationError('That username is already taken')



class CreateListForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=3, max=50, message="Title length must be between 3 and 50 syllables")])
    description = StringField('Description')
    submit = SubmitField('Create')

class CreateTaskForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    done = BooleanField('Completed')
    submit = SubmitField('Add')