from flask import Blueprint
from flask import render_template, request, flash, redirect, url_for

from flask_login import login_user, logout_user, login_required, current_user

from .forms import LoginForm, RegisterForm, TaskForm
from .models import User, Task
from .const import *
from .email import welcome_email

from . import login_manager

page = Blueprint('page', __name__)

@login_manager.user_loader
def load_user(id):
	return User.get_by_id(id)

@page.app_errorhandler(404)
def page_not_found(error):
	return render_template('errors/404.html'), 404

@page.route('/')
def index():
	return render_template('index.html', title="Proyecto")

@page.route('/login', methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('.tasks'))
	form = LoginForm(request.form)

	if request.method == 'POST' and form.validate():
		user = User.get_by_username(form.username.data)
		if user and user.verify_password(form.password.data):
			login_user(user)
			flash('Usuario autenticado exitosamente')
			return redirect(url_for('.tasks'))
		else:
			flash('Usuario o contraseña invalidos.', 'error')

	return render_template('auth/login.html', title='Login', form=form)

@page.route('/logout')
def logout():
	logout_user()
	flash('Cerraste sesión exitosamente')
	return redirect(url_for('.login'))

@page.route('/register', methods=['GET', 'POST'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('.tasks'))
	form = RegisterForm(request.form)
	if request.method == 'POST':
		if form.validate():
			user = User.create_element(form.username.data, form.password.data, form.email.data)
			flash('Usuario registrado exitosamente.')
			login_user(user)
			welcome_email(user)
			return redirect(url_for('.tasks'))

	return render_template('auth/register.html', title='Register', form=form)

@page.route('/tasks')
@page.route('/tasks/<int:page>')
@login_required
def tasks(page=1, per_page=2):
	pagination = current_user.tasks.paginate(page, per_page=per_page)
	tasks = pagination.items
	return render_template('tasks/list.html', title='Tareas', tasks=tasks, pagination=pagination, page=page)

@page.route('/tasks/new', methods=['GET', 'POST'])
@login_required
def new_task():
	form = TaskForm(request.form)
	if request.method == 'POST':
		if form.validate():
			task = Task.create_element(form.title.data, form.description.data, current_user.id)
			if task:
				flash(TASK_CREATED)
				return redirect(url_for('.tasks'))
	return render_template('tasks/new.html', title='Nueva tarea' ,form=form)

@page.route('/tasks/show/<int:task_id>')
def get_task(task_id):
	task = Task.query.get_or_404(task_id)
	return render_template('tasks/show.html', task=task)

@page.route('/tasks/edit/<int:task_id>', methods=['GET', 'POST'])
@login_required
def edit_task(task_id):
	task = Task.query.get_or_404(task_id)

	if task.user_id != current_user.id:
		abort(404)

	form = TaskForm(request.form,obj=task)
	if request.method == 'POST':
		task = Task.update_element(task.id, form.title.data, form.description.data)
		if task:
			flash(TASK_UPDATED)
			return redirect(url_for('.tasks'))
	return render_template('tasks/edit.html', title='Editar Tarea', form=form)

@page.route('/tasks/delete/<int:task_id>')
@login_required
def delete_task(task_id):
	task = Task.query.get_or_404(task_id)
	
	if task.user_id != current_user.id:
		abort(404)
	if Task.delete_element(task.id):
		flash(TASK_DELETED)
	return redirect(url_for('.tasks'))