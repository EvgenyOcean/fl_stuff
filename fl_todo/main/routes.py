from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user

main = Blueprint('main', __name__)

@main.route('/blog')
def blog():
    return render_template('blog.html')  

@main.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('todos.lists', username=current_user.username))
    else: 
        return redirect(url_for('users.login'))