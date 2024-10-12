import sqlite3
import bcrypt
from tools import GlobalSettings


class User:
	# Class representing a user with common attributes and methods.

	def __init__(self, user_id, username, password, email, role, 
		year_group=None, is_enrolled=True, failed_attempts=0, is_locked=False):
		self.user_id = user_id
		self.username = username
		self.password = password
		self.email = email
		self.role = role
		self.year_group = year_group
		self.is_enrolled = is_enrolled
		self.failed_attempts = failed_attempts
		self.is_locked = is_locked

	@classmethod
	def create_user(cls, username, password, email, **kwargs):
		# Creates a user with the given details.
		hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute(
				'''INSERT INTO users 
				(username, password, email, role, year_group, is_enrolled)
				VALUES (?, ?, ?, ?, ?, ?)''',
				(username, hashed_password, email, cls.__name__.lower(),
				kwargs.get('year_group'), kwargs.get('is_enrolled', True))
			)
			db.commit()
			user_id = cursor.lastrowid
		return cls(user_id, username, hashed_password, email, cls.__name__.lower(),
				kwargs.get('year_group'), kwargs.get('is_enrolled', True))

	@classmethod
	def validate_user(cls, username, password):
		# Check if the security feature is enabled
		security_enabled = GlobalSettings.get_security_setting()
	
		# Connect to the database and validate user credentials
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
			user_data = cursor.fetchone()
	
			if user_data:
				stored_hashed_password = user_data[2]
				failed_attempts = user_data[6]
				is_locked = user_data[7]
	
				# Check if the account is locked
				if is_locked:
					return None, True  # Return None and a flag indicating the account is locked
	
				# Validate password
				if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password):
					# Reset failed attempts on successful login
					if security_enabled:
						cursor.execute('UPDATE users SET failed_attempts = 0 WHERE user_id = ?', (user_data[0],))
					db.commit()
					return cls(user_data[0], user_data[1], stored_hashed_password, user_data[3],
						user_data[4], user_data[5], True), False  # Return user and no lock flag
	
				if security_enabled:
					# Increment failed attempts only if security is enabled
					failed_attempts += 1
					cursor.execute('UPDATE users SET failed_attempts = ? WHERE user_id = ?', (failed_attempts, user_data[0]))
	
					# Lock account if attempts exceed 3
					if failed_attempts > 3:
						cursor.execute('UPDATE users SET is_locked = ? WHERE user_id = ?', (True, user_data[0]))
	
				db.commit()
				return None, False  # Return None and no lock flag if credentials are invalid
	
		return None, False  # Return None and no lock flag if user not found


	@classmethod
	def fetch_user(cls, user_id):
		# Fetches a user by user_id from the database.
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('SELECT user_id, username, email, role FROM users WHERE user_id = ?', 
				(user_id,))
			user_data = cursor.fetchone()
			if user_data:
				return cls(user_data[0], user_data[1], None, user_data[2], user_data[3])  
			return None  # Return None if no user found

	@classmethod
	def fetch_all_users(cls):
		# Fetches all users from the database.
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('SELECT user_id, username, email, role, year_group, is_enrolled FROM users')
			users_data = cursor.fetchall()
			return [cls(user_id, username, None, email, role, year_group, is_enrolled)
					for user_id, username, email, role, year_group, is_enrolled in users_data]

	@classmethod
	def update_user(cls, user_id, username, email, role):
		# Updates the user's details in the database.
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('''UPDATE users SET username = ?, email = ?, role = ? 
							WHERE user_id = ?''',
				(username, email, role, user_id))
			db.commit()

	@classmethod
	def delete_user(cls, user_id):
		# Deletes a user by user_id from the database.
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('DELETE FROM users WHERE user_id = ?', (user_id,))
			db.commit()

	@classmethod
	def reset_password(cls, user_id, new_password='password'):
		# Resets the user's password.
		hashed_password = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('UPDATE users SET password = ? WHERE user_id = ?',
				(hashed_password, user_id))
			db.commit()
		return True


class Student(User):
	# Class representing a student, inheriting from User.

	def __init__(self, user_id, username, password, email, year_group, is_enrolled=True):
		super().__init__(user_id, username, password, email, 'student', year_group, is_enrolled)

	@classmethod
	def create_student(cls, username, password, email, year_group, is_enrolled=True):
		# Creates a student with the given details.
		return cls.create_user(username, password, email, year_group=year_group, 
				is_enrolled=is_enrolled)


class Teacher(User):
	# Class representing a teacher, inheriting from User.

	def __init__(self, user_id, username, password, email):
		super().__init__(user_id, username, password, email, 'teacher')

	@classmethod
	def create_teacher(cls, username, password, email):
		# Creates a teacher with the given details.
		return cls.create_user(username, password, email)


class Admin(User):
	# Class representing an admin, inheriting from User.

	def __init__(self, user_id, username, password, email):
		super().__init__(user_id, username, password, email, 'admin')

	@classmethod
	def create_admin(cls, username, password, email):
		# Creates an admin with the given details.
		return cls.create_user(username, password, email)