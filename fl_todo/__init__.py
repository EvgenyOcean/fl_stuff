import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bcrypt import Bcrypt



app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login' #don't forget this one
login_manager.login_message_category = 'info'
bcrypt = Bcrypt(app)

from . import models
from . import routes