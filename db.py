import sqlite3
import bcrypt

import sqlite3

# Function to initialize the database
def init_db():
	# Connect to the database
	with sqlite3.connect('database.db') as db:
		cursor = db.cursor()

		# Create users table
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS users (
				user_id INTEGER PRIMARY KEY AUTOINCREMENT,
				username TEXT NOT NULL,
				password TEXT NOT NULL,
				email TEXT NOT NULL,
				role TEXT NOT NULL,
				year_group INTEGER,
				is_enrolled BOOLEAN DEFAULT 1,
				failed_attempts INTEGER DEFAULT 0,
				is_locked BOOLEAN DEFAULT 0
			)
		''')

		# Create subjects table
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS subjects (
				subject_id INTEGER PRIMARY KEY AUTOINCREMENT,
				name TEXT NOT NULL,
				teacher_id INTEGER,
				FOREIGN KEY (teacher_id) REFERENCES users(user_id) 
				ON DELETE SET NULL
			)
		''')

		# Create timetable table
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS timetable (
				timetable_id INTEGER PRIMARY KEY AUTOINCREMENT,
				user_id INTEGER,
				subject_id INTEGER,
				day_of_week TEXT NOT NULL,
				start_time TIME NOT NULL,
				end_time TIME NOT NULL,
				FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
				FOREIGN KEY (subject_id) REFERENCES subjects(subject_id) 
				ON DELETE CASCADE
			)
		''')

		# Create global settings table
		cursor.execute('''
			CREATE TABLE IF NOT EXISTS global_settings (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				security_enabled BOOLEAN DEFAULT 1
			)
		''')

		cursor.execute('INSERT INTO global_settings (security_enabled) VALUES (1)')

		# Commit changes
		db.commit()
