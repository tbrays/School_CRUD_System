import re
import logging
from flask import Flask, render_template, request, redirect, url_for, session, flash
from user import User, Student, Teacher, Admin
from timetable import Timetable
from subject import Subject
from tools import GlobalSettings, is_strong_password
from db import init_db
from test_data import (
		create_default_admin,
		add_subjects,
		add_student_with_timetable,
		add_teacher_with_timetable
)

app = Flask(__name__, template_folder="public")
# Set the secret key from the environment variable
app.secret_key = '3f4e55bfa95d41e6a6f2e9196f3f8bc9'  # Secret key for sessions

# Configure logging
logging.basicConfig(
	filename='login.log',
	level=logging.INFO,
	format='%(asctime)s - %(levelname)s - %(message)s'
)

# Initialize the database
init_db()

# Add default admin, subjects, student, and teacher data
create_default_admin()
add_subjects()
add_student_with_timetable()
add_teacher_with_timetable()

@app.route('/')
def home_page():
	# Render the home page
	return render_template('home.html')


@app.route('/login', methods=['GET', 'POST'])
def login_page():
	if request.method == 'POST':
		username = request.form.get('username')
		password = request.form.get('password')

		# Validate user credentials using the User class method
		user, is_locked = User.validate_user(username, password)

		if user:
			# Successful login
			session['user_id'] = user.user_id
			session['username'] = user.username
			session['role'] = user.role

			# Log successful login
			app.logger.info(f'Successful login for user: {username}')
			return redirect(url_for('dashboard_page'))  # Redirect to dashboard
		else:
			# Check if the account is locked
			if is_locked:
				flash('Your account is locked due to too many failed login attempts.', 'error')
				return render_template('login.html')  # Render login form with locked error

			flash('Invalid username or password. Please try again.', 'error')
			app.logger.warning(f'Failed login attempt for user: {username}')

	return render_template('login.html')  # Render login form on GET request


@app.route('/logout')
def logout():
	# Log out the user and clear the session
	session.clear()  # Remove all session data
	return redirect(url_for('home_page'))  # Redirect to home page


@app.route('/register', methods=['GET', 'POST'])
def register_page():
	# Handle user registration
	if request.method == 'POST':
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		role = request.form['role']

		# Check if the password is strong
		if not is_strong_password(password):
			# Render the registration form again with an error message
			error_message = "Password must be at least 8 characters long, contain an uppercase letter, a lowercase letter, a number, and a special character."
			return render_template('register.html', error=error_message)

		try:
			if role == 'student':
				year_group = request.form.get('year_group', None)
				is_enrolled = request.form.get('enrolled', 'false').lower() == 'true'
				Student.create_student(username, password, email, year_group, is_enrolled)

		except Exception:
			return redirect(url_for('login_page'))

		return redirect(url_for('login_page'))  # Redirect to login after registration

	return render_template('register.html')  # Render registration form if GET request


@app.route('/dashboard')
def dashboard_page():
	# Render the dashboard page for the logged-in user
	current_user = session.get('username', None)
	role = session.get('role')
	return render_template('dashboard.html', role=role, current_user=current_user)


@app.route('/timetable', methods=['GET'])
def timetable_page():
	# Display the timetable for the logged-in user
	if 'user_id' not in session:
		return redirect(url_for('login_page'))

	user_id = session['user_id']
	timetable_entries = Timetable.get_timetable(user_id)  # Fetch timetable entries
	return render_template('timetable.html', timetable=timetable_entries, student_id=user_id)


@app.route('/manage_users', methods=['GET', 'POST'])
def manage_users_page():
	# Handle user management actions: add, delete, or reset password
	if request.method == 'POST' and 'add_user' in request.form:
		username = request.form['username']
		email = request.form['email']
		password = request.form['password']
		role = request.form['role']

		# Check if the password is strong
		if not is_strong_password(password):
			error_message = (
				"Password must be at least 8 characters long, "
				"contain an uppercase letter, a lowercase letter, "
				"a number, and a special character."
			)
			users = User.fetch_all_users()
			return render_template('manage_users.html', users=users, error=error_message)

		try:
			if role == 'student':
				year_group = request.form.get('year_group', None)
				is_enrolled = request.form.get('enrolled', 'false').lower() == 'true'
				Student.create_student(username, password, email, year_group, is_enrolled)

			elif role == 'teacher':
				Teacher.create_teacher(username, password, email)

			elif role == 'admin':
				Admin.create_admin(username, password, email)

		except Exception:
			return redirect(url_for('manage_users_page'))

		return redirect(url_for('manage_users_page'))

	if request.method == 'POST' and 'delete_user' in request.form:
		user_id = request.form['user_id']
		User.delete_user(user_id)  # Handle user deletion
		return redirect(url_for('manage_users_page'))

	if request.method == 'POST' and 'reset_password' in request.form:
		user_id = request.form['user_id']
		User.reset_password(user_id)  # Reset password to default 'password'
		return redirect(url_for('manage_users_page'))

	users = User.fetch_all_users()  # Fetch all users for display
	return render_template('manage_users.html', users=users)


@app.route('/edit_user/<int:user_id>', methods=['GET', 'POST'])
def edit_user_page(user_id):
	# Handle user edit actions: update username, email, or role
	if request.method == 'POST':
		new_username = request.form['username']
		new_email = request.form['email']
		new_role = request.form['role']
		User.update_user(user_id, new_username, new_email, new_role)
		return redirect(url_for('manage_users_page'))

	user = User.fetch_user(user_id)
	if user:
		return render_template('edit_user.html', user=user)
	else:
		return redirect(url_for('manage_users_page'))


@app.route('/manage_timetable', methods=['GET', 'POST'])
def manage_timetable_page():
	# Handle timetable management: add subjects, entries, or delete entries
	all_users = User.fetch_all_users()
	students = [user for user in all_users if user.role == 'student']
	teachers = [user for user in all_users if user.role == 'teacher']
	subjects = Subject.fetch_all_subjects()

	if request.method == 'POST' and 'subject_name' in request.form:
		subject_name = request.form['subject_name']
		Subject.create_subject(subject_name)
		return redirect(url_for('manage_timetable_page'))

	if request.method == 'POST' and 'user_id' in request.form and 'subject_id' in request.form:
		user_id = request.form['user_id']
		subject_id = request.form['subject_id']
		day_of_week = request.form['day_of_week']
		start_time = request.form['start_time']
		end_time = request.form['end_time']
		Timetable.create_timetable_entry(user_id, subject_id, day_of_week, start_time, end_time)
		return redirect(url_for('manage_timetable_page'))

	if request.method == 'POST' and 'entry_id' in request.form:
		entry_id = request.form['entry_id']
		Timetable.delete_timetable_entry(entry_id)
		return redirect(url_for('manage_timetable_page'))

	user_id = request.args.get('user_id')
	timetable = []
	if user_id:
		timetable = Timetable.get_timetable(user_id)

	return render_template('manage_timetable.html', students=students, teachers=teachers,
							 timetable=timetable, subjects=subjects)


@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
	if request.method == 'POST':
		current_status = GlobalSettings.get_security_setting()
		new_status = not current_status
		GlobalSettings.update_security_setting(new_status)
		return redirect(url_for('settings_page'))  

	# Handle GET request - render settings page
	security_enabled = GlobalSettings.get_security_setting()
	return render_template('settings.html', security_enabled=security_enabled)  # Render the settings page
	

if __name__ == "__main__":
	app.run(host='127.0.0.1', port=5000)
	
