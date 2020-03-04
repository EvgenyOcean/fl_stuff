from flask import Blueprint, render_template, request, redirect, flash, url_for, abort
from fl_todo import db
from flask_login import login_required, current_user
from .forms import CreateListForm, CreateTaskForm  
from fl_todo.models import Task, List



todos = Blueprint('todos', __name__)

@todos.route('/users/<string:username>/lists', methods=['POST', 'GET'])
@login_required
def lists(username):
    if current_user.username == username:
        lists = List.query.filter_by(user_id=current_user.id)
        form = CreateListForm()
        if request.method == "POST" and form.validate_on_submit():
            new_list = List(title=form.title.data, description=form.description.data, user=current_user)
            db.session.add(new_list)
            db.session.commit()
            return redirect(url_for('todos.lists', username=current_user.username))
        return render_template('lists.html', form=form, lists=lists)
    else:
        return abort(403)

@todos.route('/users/<string:username>/<int:id>/edit', methods=['POST', 'GET'])
@login_required
def edit_list(username, id):
    if current_user.username == username:
        list = List.query.filter_by(id=id).first_or_404()
        form = CreateListForm()
        if request.method == 'POST' and form.validate_on_submit():
            list.title = form.title.data
            list.description = form.description.data
            db.session.commit()
            return redirect(url_for('todos.lists', username=current_user.username))
        return render_template('editlist.html', form=form, list=list)
    
    return abort(403)

@todos.route('/users/<string:username>/<int:id>/delete', methods=['POST'])
@login_required
def delete_list(username, id):
    if current_user.username == username:
        list = List.query.get_or_404(id)
        db.session.delete(list)
        db.session.commit()
        return redirect(url_for('todos.lists', username=current_user.username))

    return abort(403)

@todos.route('/users/<string:username>/<int:id>', methods=['POST', 'GET'])
@login_required
def tasks(username, id):
    if current_user.username == username:
        form = CreateTaskForm()
        list = List.query.filter_by(id=id).first_or_404()
        tasks = Task.query.filter_by(list=list)
        if request.method == "POST" and form.validate_on_submit():
            new_task = Task(name=form.name.data, list_id=list.id)
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for('todos.tasks', username=current_user.username, id=list.id))
        return render_template('tasks.html', tasks=tasks, list=list, form=form)
    return abort(403)

@todos.route('/users/<string:username>/<int:list_id>/<int:task_id>', methods=['POST', 'GET'])
@login_required
def edit_task(username, list_id, task_id):
    if current_user.username == username: 
        list = List.query.get_or_404(list_id)
        task = Task.query.get_or_404(task_id)
        if task.list == list:
            form = CreateTaskForm()
            if request.method == 'POST' and form.validate_on_submit():
                task.name = form.name.data
                task.done = form.done.data
                db.session.commit()
                return redirect(url_for('todos.tasks', username=current_user.username, id=list.id))
        else: 
            return abort(404)
        return render_template('edittask.html', form=form, task=task)
    else: 
        return abort(403)

@todos.route('/users/<string:username>/<int:list_id>/<int:task_id>/delete', methods=['POST'])
@login_required
def task_delete(username, list_id, task_id):
    if current_user.username == username: 
            list = List.query.get_or_404(list_id)
            task = Task.query.get_or_404(task_id)
            if task.list == list:
                db.session.delete(task)
                db.session.commit()
                return redirect(url_for('todos.tasks', username=current_user.username, id=list.id))
            else: 
                return abort(404)
    else: 
        return abort(403)