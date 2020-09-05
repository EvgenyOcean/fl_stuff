import os
from flask import Flask
from .commands import create_tables
from .extensions import db, login_manager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from fl_todo.config import Config

bcrypt = Bcrypt()
mail = Mail()

login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'

def create_app(config=Config):
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)

    from fl_todo.posts.routes import posts
    from fl_todo.users.routes import users
    from fl_todo.todos.routes import todos

    app.register_blueprint(posts)
    app.register_blueprint(users)
    app.register_blueprint(todos)

    app.cli.add_command(create_tables)

    return app