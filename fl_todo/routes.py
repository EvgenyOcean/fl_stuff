from . import app, bcrypt, db
from flask import render_template, request, redirect, flash, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from .forms import UserRegisterForm, UserLoginForm, CreateListForm, CreateTaskForm
from .models import User, List, Task


@app.route('/blog')
def blog():
    return render_template('blog.html')  

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('user_lists', username=current_user.username))
    else: 
        return redirect(url_for('login'))

@app.route('/<string:username>', methods=['POST', 'GET'])
@login_required
def user_lists(username):
    if current_user.username == username:
        lists = List.query.filter_by(user_id=current_user.id)
        form = CreateListForm()
        if request.method == "POST" and form.validate_on_submit():
            new_list = List(title=form.title.data, description=form.description.data, user=current_user)
            db.session.add(new_list)
            db.session.commit()
            return redirect(url_for('user_lists'))
        return render_template('lists.html', form=form, lists=lists)
    else:
        return abort(403)

@app.route('/<string:username>/<int:id>', methods=['POST', 'GET'])
@login_required
def list_tasks(username, id):
    if current_user.username == username:
        form = CreateTaskForm()
        list = List.query.filter_by(id=id).first_or_404()
        tasks = Task.query.filter_by(list=list) #Maybe a fix needed
        if request.method == "POST" and form.validate_on_submit():
            new_task = Task(name=form.name.data, list_id=list.id)
            db.session.add(new_task)
            db.session.commit()
            # return redirect(url_for('list_tasks')) gotta put it back to work
        return render_template('tasks.html', tasks=tasks, list=list, form=form)

@app.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserRegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Welcome aboard!', category='success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = UserLoginForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Hey, how are you today? :)', category="success")
            if (request.args.get('next')):
                print(request.args.get('next'))
                return redirect(request.args.get('next'))
            return redirect(url_for('home'))
        else: 
            flash('Wow, that didn\'t seem correct! :(', category="danger")
    return render_template('login.html', form=form)

@login_required
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('blog'))


@app.route('/account')
@login_required
def account():
    return 'WAIT!'
