from . import app, bcrypt, db, mail
from flask import render_template, request, redirect, flash, url_for, abort
from flask_login import login_user, logout_user, login_required, current_user
from .forms import UserRegisterForm, UserLoginForm, CreateListForm, CreateTaskForm, UserEmailForResetForm, UserPasswordResetForm
from .models import User, List, Task
from flask_mail import Message


@app.route('/blog')
def blog():
    return render_template('blog.html')  

@app.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('user_lists', username=current_user.username))
    else: 
        return redirect(url_for('login'))

@app.route('/users/<string:username>/lists', methods=['POST', 'GET'])
@login_required
def user_lists(username):
    if current_user.username == username:
        lists = List.query.filter_by(user_id=current_user.id)
        form = CreateListForm()
        if request.method == "POST" and form.validate_on_submit():
            new_list = List(title=form.title.data, description=form.description.data, user=current_user)
            db.session.add(new_list)
            db.session.commit()
            return redirect(url_for('user_lists', username=current_user.username))
        return render_template('lists.html', form=form, lists=lists)
    else:
        return abort(403)

@app.route('/users/<string:username>/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_list(username, id):
    if current_user.username == username:
        list = List.query.filter_by(id=id).first_or_404()
        form = CreateListForm()
        if request.method == 'POST' and form.validate_on_submit():
            list.title = form.title.data
            list.description = form.description.data
            db.session.commit()
            return redirect(url_for('user_lists', username=current_user.username))
        return render_template('editlist.html', form=form, list=list)
    
    return abort(403)

@app.route('/users/<string:username>/<int:id>/delete', methods=['POST'])
@login_required
def delete_list(username, id):
    if current_user.username == username:
        list = List.query.get_or_404(id)
        print(id)
        print(list)
        db.session.delete(list)
        db.session.commit()
        return redirect(url_for('user_lists', username=current_user.username))

    return abort(403)

@app.route('/users/<string:username>/<int:id>', methods=['POST', 'GET'])
@login_required
def tasks(username, id):
    if current_user.username == username:
        form = CreateTaskForm()
        list = List.query.filter_by(id=id).first_or_404()
        tasks = Task.query.filter_by(list=list) #Maybe a fix needed
        if request.method == "POST" and form.validate_on_submit():
            new_task = Task(name=form.name.data, list_id=list.id)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('tasks', username=current_user.username, id=list.id)) #to prevent data from being resent
        return render_template('tasks.html', tasks=tasks, list=list, form=form)
    return abort(403)

@app.route('/users/<string:username>/<int:list_id>/<int:task_id>', methods=['POST', 'GET'])
@login_required
def edit_task(username, list_id, task_id):
    if current_user.username == username: 
        list = List.query.get_or_404(list_id)
        task = Task.query.get_or_404(task_id)
        #Does the list contain the task? 
        if task.list == list:
            form = CreateTaskForm()
            if request.method == 'POST' and form.validate_on_submit():
                task.name = form.name.data
                task.done = form.done.data
                db.session.commit()
                return redirect(url_for('tasks', username=current_user.username, id=list.id))
        else: 
            return abort(404)
        return render_template('edittask.html', form=form, task=task)
    else: 
        return abort(403)

@app.route('/users/<string:username>/<int:list_id>/<int:task_id>/delete', methods=['POST'])
@login_required
def task_delete(username, list_id, task_id):
    if current_user.username == username: 
            list = List.query.get_or_404(list_id)
            task = Task.query.get_or_404(task_id)
            #Does the list contains the task? 
            if task.list == list:
                db.session.delete(task)
                db.session.commit()
                return redirect(url_for('tasks', username=current_user.username, id=list.id))
            else: 
                return abort(404)
    else: 
        return abort(403)

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

# ========================= > Reset Password Area

def send_message(user):
    token = user.request_token()
    msg = Message('Reset Password Request', 
                  sender="noreply@demo.com",
                  recipients=[user.email])
    msg.body = f'''Please follow the link to reset your password: 
    {url_for('new_password', token=token, _external=True)} 
    If you have no idea whats going on, then just ignore the message. Have a good day :) 
    '''

    mail.send(msg)

@app.route('/reset', methods=['POST', 'GET'])
def email_token():
    if current_user.is_authenticated: 
        return redirect(url_for('blog'))
    form = UserEmailForResetForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() #adding a server error could come in handy
        send_message(user)
        flash('The message was successfully sent!', 'success')
        return redirect(url_for('blog'))
    else:
        return render_template('emailtoken.html', form=form)

@app.route('/resetpass/<token>', methods=['POST', 'GET'])
def new_password(token):
    form = UserPasswordResetForm()
    user = User.check_token(token)
    if user is None: 
        flash('Token is invalid or has been expired!', 'danger')
        return redirect(url_for('blog'))
    if request.method == 'POST' and form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Congratulations! Your password was successfully updated!', 'success')
        return redirect(url_for('home'))
    return render_template('passwordreset.html', form=form)

# ========================= > Reset Password Area
