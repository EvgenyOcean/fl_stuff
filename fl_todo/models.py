from datetime import datetime
from . import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(16), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(60), nullable=False)
    avatar = db.Column(db.String(20), nullable=False, default='default.png')

class List(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(30), nullable=False)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('lists', lazy=True, cascade="all, delete-orphan"))

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    done = db.Column(db.Boolean, default=False, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'), nullable=False)
    list = db.relationship('List', backref=db.backref('tasks', lazy=True, cascade="all, delete-orphan"))