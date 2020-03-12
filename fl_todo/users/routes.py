from flask import Blueprint, request, render_template, redirect, flash, url_for, abort
from fl_todo import db, bcrypt, mail
from flask_login import login_user, logout_user, login_required, current_user
from .forms import (UserAccountForm, UserEmailForResetForm, 
                   UserLoginForm, UserPasswordResetForm, UserRegisterForm)
from fl_todo.models import User
from .utils import edit_avatar, send_message



users = Blueprint('users', __name__)

@users.route('/register', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('posts.home'))
    form = UserRegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Welcome aboard!', category='success')
        return redirect(url_for('users.login'))
    return render_template('register.html', form=form)

@users.route('/login', methods=['POST', 'GET'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('posts.home'))
    form = UserLoginForm()
    if request.method == "POST" and form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            flash('Hey, how are you today? :)', category="success")
            if (request.args.get('next')):
                print(request.args.get('next'))
                return redirect(request.args.get('next'))
            return redirect(url_for('posts.home'))
        else: 
            flash('Wow, that didn\'t seem correct! :(', category="danger")
    return render_template('login.html', form=form)

@login_required
@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('posts.blog'))

@users.route('/account', methods=['POST', 'GET'])
@login_required
def account():
    form = UserAccountForm()
    user = User.query.get(current_user.id)
    if request.method == 'POST' and form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        if form.avatar.data:
            new_name = edit_avatar(form.avatar.data)
            user.avatar = new_name
        db.session.commit()
        flash('Your account was successfully updated', 'success')
        return redirect(url_for('users.account'))
    return render_template('account.html', form=form, user=user)

@users.route('/reset', methods=['POST', 'GET'])
def email_token():
    if current_user.is_authenticated: 
        return redirect(url_for('posts.blog'))
    form = UserEmailForResetForm()
    if request.method == 'POST' and form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first() #adding a server error could come in handy
        send_message(user)
        flash('The message was successfully sent!', 'success')
        return redirect(url_for('posts.blog'))
    else:
        return render_template('emailtoken.html', form=form)

@users.route('/resetpass/<token>', methods=['POST', 'GET'])
def new_password(token):
    form = UserPasswordResetForm()
    user = User.check_token(token)
    if user is None: 
        flash('Token is invalid or has been expired!', 'danger')
        return redirect(url_for('posts.blog'))
    if request.method == 'POST' and form.validate_on_submit():
        hashed_pw = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_pw
        db.session.commit()
        flash('Congratulations! Your password was successfully updated!', 'success')
        return redirect(url_for('posts.home'))
    return render_template('passwordreset.html', form=form)