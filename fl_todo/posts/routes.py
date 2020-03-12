from flask import Blueprint, render_template, redirect, url_for, request, current_app, flash, abort
from fl_todo import db
from flask_login import current_user, login_required
from .forms import CreatePostForm
from fl_todo.models import User, Post

posts = Blueprint('posts', __name__)

@posts.route('/blog')
def blog():
    posts = Post.query.all()
    return render_template('blog.html', posts=posts)  

@posts.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('todos.lists', username=current_user.username))
    else: 
        return redirect(url_for('users.login'))

@posts.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = CreatePostForm()
    if form.validate_on_submit() and request.method == 'POST': 
        new_post = Post(title=form.title.data, text=form.text.data, user=current_user)
        db.session.add(new_post)
        db.session.commit()
        flash('Look, you got your post published!', 'success') 
        return redirect(url_for('posts.blog'))
    return render_template('create_post.html', form=form)

@posts.route('/view_post/<int:post_id>')
def view_post(post_id):
    post = Post.query.filter_by(id=post_id).first_or_404()
    return render_template('view_post.html', post=post) 

@posts.route('/update_post/<int:post_id>', methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CreatePostForm()
    if current_user == post.user:
        if request.method == 'POST' and form.validate_on_submit():
            post.title = form.title.data
            post.text = form.text.data
            db.session.commit()
            flash('Your post was successfully updated', 'success')
            return redirect(url_for('posts.blog'))
    else: 
        return abort(403)
    return render_template('update_post.html', form=form, post=post)

@posts.route('/delete_post/<int:post_id>', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if current_user == post.user: 
        db.session.delete(post)
        db.session.commit()
        flash('And they never saw it again! ;)', 'success')
        return redirect(url_for('posts.blog'))
    else: 
        return abort(403)

