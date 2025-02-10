# tasks.py
from flask import Blueprint, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
db = SQLAlchemy()

models_blueprint = Blueprint('models', __name__)



class UserData(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


# @tasks_blueprint.route('/tasks', methods=['GET', 'POST'])
# def tasks():
#     if request.method == 'POST':
#         new_task_title = request.form.get('title')
#         new_task = Task(title=new_task_title)
#         db.session.add(new_task)
#         db.session.commit()

#     tasks = Task.query.all()
#     return render_template('tasks/tasks.html', tasks=tasks)

# @tasks_blueprint.route('/tasks/<int:task_id>/delete', methods=['POST'])
# def delete_task(task_id):
#     task = Task.query.get_or_404(task_id)
#     db.session.delete(task)
#     db.session.commit()
#     return redirect(url_for('tasks.tasks'))
