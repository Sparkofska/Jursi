from wtforms import Form, StringField, PasswordField, validators
from flask import render_template, request, flash, abort, redirect, url_for
from flask_login import login_user, logout_user, current_user, login_required

class LoginForm(Form):
	username = StringField('Username', [validators.DataRequired(), validators.Length(min=4, max=25, message="Username's length must be between 4 and 25")])
	password = PasswordField('Password', [validators.DataRequired()])

predefined_users = [('admin', 'admin')]

class User:
	def __init__(self, username, password):
		self.username = username
		self.password = password
		self.id = ord(username[0]) # TODO set id accordingly. For now its just the number of first letter
	
	def __str__(self):
		return 'User(%s)' % self.username
	
	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		return str(self.id)  # python 3

	def get(id):
		for pre_user in predefined_users:
			if pre_user[0].startswith(chr(id)):
				return User(pre_user[0], pre_user[1])
		return None



def login():
	form = LoginForm(request.form)
	if request.method == 'POST':
		if form.validate():
			if (form.username.data, form.password.data) in predefined_users:
				user = User(form.username.data, form.password.data)
				login_user(user)
				flash('User ' + user.username + ' logged in successfully')
		
				# is_safe_url should check if the url is safe for redirects.
				# See http://flask.pocoo.org/snippets/62/ for an example.
				#if not is_safe_url(next):
				#	return abort(400)
		
				return redirect(url_for('dashboard'))
			flash('Wrong username or password')
		
	return render_template('LoginPage.html', form=form)

def logout():
    logout_user()
    return redirect('/login/')
