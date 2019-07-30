from wtforms import Form
from wtforms import validators
from wtforms import StringField, PasswordField, BooleanField, HiddenField, TextAreaField
from wtforms.fields.html5 import EmailField

from .models import User

#def username_validator(form, field):
#	if field.data == 'codi' or field.data == 'Codi':
#		raise validators.ValidationError('El username no esta permitido')

def length_honeypot(form, field):
	if len(field.data) > 0:
		raise validators.ValidationError('Solo humanos pueden completar el registro.')

class LoginForm(Form):
	username = StringField('Username', [
		validators.length(min=4, max=50, message='El username se encuentra fuera de rango.')
	])
	password = PasswordField('Password', [
		validators.Required('El password es requerido.')
	])

class RegisterForm(Form):
	username = StringField('Username', [
		validators.length(min=4, max=50, message='El username se encuentra fuera de rango.')
	])
	email = EmailField('Email', [
		validators.length(min=6, max=100),
		validators.Required(message='El email es requerido.'),
		validators.Email(message='Ingrese un email valido.')
	])
	password = PasswordField('Password', [
		validators.Required('El password es requerido.'),
		validators.EqualTo('confirm_password', message='La contraseña no coincide.')
	])
	confirm_password = PasswordField('Confirm Password')
	accept = BooleanField('Acepto terminos y condiciones', [
		validators.DataRequired()
	])
	honeypot = HiddenField("", [length_honeypot])

	def validate_username(self, username):
		if User.get_by_username(username.data):
			raise validators.ValidationError('El username ya se encuentra en uso.')

	def validate_email(self, email):
		if User.get_by_email(email.data):
			raise validators.ValidationError('El email ya se encuentra en uso.')
	
	def validate(self):
		if not Form.validate(self):
			return False
		if len(self.password.data) < 3:
			self.password.errors.append('El password es demasiado corto')
			return False
		return True

class TaskForm(Form):
	title = StringField('Titulo', [
		validators.length(min=4, max=50, message='Titulo fuera de rango.'),
		validators.DataRequired(message='El título es requerido.')
	])
	description = TextAreaField('Descripcion', [
		validators.DataRequired(message='La descripcion es requerida.')
	], render_kw={'rows': 5})