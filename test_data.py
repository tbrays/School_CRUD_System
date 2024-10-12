import sqlite3
import bcrypt

# Function to create the default admin
def create_default_admin():
	# Define default admin credentials
	default_admin_username = "admin"
	default_admin_email = "admin@example.com"
	default_admin_password = "admin123"
	default_admin_role = "admin"

	# Connect to the database
	with sqlite3.connect('database.db') as db:
		cursor = db.cursor()

		# Check if an admin already exists
		cursor.execute('SELECT * FROM users WHERE role = ?', (default_admin_role,))
		admin = cursor.fetchone()

		# If no admin exists, create the default admin
		if admin is None:
			hashed_password = bcrypt.hashpw(
				default_admin_password.encode('utf-8'),
				bcrypt.gensalt()
			)

			# Insert the default admin into the users table
			cursor.execute('''
				INSERT INTO users (username, email, password, role, failed_attempts, is_locked)
				VALUES (?, ?, ?, ?, ?, ?)
			''', (default_admin_username, default_admin_email, 
					hashed_password, default_admin_role, 0, 0))

			db.commit()
			print(f"Default admin user '{default_admin_username}' has been created.")
		else:
			print("Admin user already exists.")

# Function to add subjects to the database
def add_subjects():
	subjects = ["Mathematics", "English", "History", 
				"Biology", "Chemistry"]

	with sqlite3.connect('database.db') as db:
		cursor = db.cursor()

		for subject in subjects:
			# Check if the subject already exists
			cursor.execute('SELECT * FROM subjects WHERE name = ?', 
							 (subject,))
			if not cursor.fetchone():  
				# If no subject is found, proceed to insert
				cursor.execute('INSERT INTO subjects (name) VALUES (?)', 
								 (subject,))

		db.commit()
		print(f"Successfully added {len(subjects)} subjects.")

# Function to add a student with a timetable
def add_student_with_timetable():
	# Define student details
	username = 'john_doe'
	password = 'password123'
	email = 'john@example.com'
	year_group = 10  # Example year group (as an integer)

	# Hash the password
	hashed_password = bcrypt.hashpw(password.encode('utf-8'), 
									bcrypt.gensalt())

	# Define timetable entries with subject IDs, days, start, and end times
	timetable_entries = [
		(1, 'Monday', '9:00 AM', '10:00 AM'),   # Subject ID 1 for Mathematics
		(2, 'Monday', '10:00 AM', '11:00 AM'),  # Subject ID 2 for English
		(3, 'Wednesday', '11:00 AM', '12:00 PM'), # Subject ID 3 for History
		(4, 'Friday', '1:00 PM', '2:00 PM'),    # Subject ID 4 for Biology
		(5, 'Thursday', '2:00 PM', '3:00 PM')   # Subject ID 5 for Chemistry
	]

	with sqlite3.connect('database.db') as db:
		cursor = db.cursor()

		# Check if the student already exists
		cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', 
						 (username, email))
		existing_user = cursor.fetchone()

		if existing_user:
			print(f"User with username '{username}' or email '{email}' already exists. No action taken.")
			return  # Exit if the user already exists

		# Insert the student into the users table
		cursor.execute('''
			INSERT INTO users (username, password, email, role, year_group, is_enrolled, failed_attempts, is_locked) 
			VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
						 (username, hashed_password, email, 'student', 
						year_group, 1, 0, 0))  # is_enrolled is set to 1 (True), defaults for failed_attempts and is_locked

		student_id = cursor.lastrowid  # Get the ID of the newly created student

		# Insert the timetable for the student using entries
		for subject_id, day_of_week, start_time, end_time in timetable_entries:
			cursor.execute('''
				INSERT INTO timetable (user_id, subject_id, day_of_week, 
										 start_time, end_time) 
				VALUES (?, ?, ?, ?, ?)''',
							 (student_id, subject_id, day_of_week, 
							start_time, end_time))

		db.commit()
		print(f"Successfully added student {username} with timetable.")

# Function to add a teacher with a timetable
def add_teacher_with_timetable():
	# Define teacher details
	username = 'jane_smith'
	password = 'password1234'
	email = 'jane@example.com'

	# Hash the password
	hashed_password = bcrypt.hashpw(password.encode('utf-8'), 
									bcrypt.gensalt())

	# Define timetable entries with subject IDs, days, start, and end times
	timetable_entries = [
		(1, 'Monday', '9:00 AM', '10:00 AM'),    # Subject ID 1 for Mathematics
		(2, 'Tuesday', '10:00 AM', '11:00 AM'),  # Subject ID 2 for English
		(3, 'Wednesday', '11:00 AM', '12:00 PM'),# Subject ID 3 for History
		(4, 'Thursday', '1:00 PM', '2:00 PM'),   # Subject ID 4 for Biology
		(5, 'Friday', '2:00 PM', '3:00 PM')      # Subject ID 5 for Chemistry
	]

	with sqlite3.connect('database.db') as db:
		cursor = db.cursor()

		# Check if the teacher already exists
		cursor.execute('SELECT * FROM users WHERE username = ? OR email = ?', 
						 (username, email))
		existing_user = cursor.fetchone()

		if existing_user:
			print(f"Teacher with username '{username}' or email '{email}' already exists. No action taken.")
			return  # Exit if the teacher already exists

		# Insert the teacher into the users table
		cursor.execute('''
			INSERT INTO users (username, password, email, role, failed_attempts, is_locked) 
			VALUES (?, ?, ?, ?, ?, ?)''',
						 (username, hashed_password, email, 'teacher', 0, 0))  # Set defaults for failed_attempts and is_locked

		teacher_id = cursor.lastrowid  # Get the ID of the newly created teacher

		# Update subjects to assign the teacher to subjects
		for subject_id, _, _, _ in timetable_entries:
			cursor.execute('''
				UPDATE subjects SET teacher_id = ? WHERE subject_id = ?''',
							 (teacher_id, subject_id))

		# Insert the timetable for the teacher
		for subject_id, day_of_week, start_time, end_time in timetable_entries:
			cursor.execute('''
				INSERT INTO timetable (user_id, subject_id, day_of_week, 
										 start_time, end_time) 
				VALUES (?, ?, ?, ?, ?)''',
							 (teacher_id, subject_id, day_of_week, 
							start_time, end_time))

		db.commit()
		print(f"Successfully added teacher {username} with timetable.")
