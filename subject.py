import sqlite3


class Subject:
	# Class for managing subjects.

	def __init__(self, subject_id, name, teacher_id=None):
		self.subject_id = subject_id
		self.name = name
		self.teacher_id = teacher_id

	@classmethod
	def create_subject(cls, name, teacher_id=None):
		# Creates a subject with the given details.
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('INSERT INTO subjects (name, teacher_id) VALUES (?, ?)', 
				(name, teacher_id))
			db.commit()
			return cls(cursor.lastrowid, name, teacher_id)

	@classmethod
	def delete_subject(cls, subject_id):
		# Deletes a subject by subject_id.
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('DELETE FROM subjects WHERE subject_id = ?', (subject_id,))
			db.commit()

	@classmethod
	def fetch_all_subjects(cls):
		# Fetches all subjects from the database.
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('SELECT subject_id, name, teacher_id FROM subjects')
			subjects_data = cursor.fetchall()
			return [cls(subject[0], subject[1], subject[2]) for subject in subjects_data]

	@classmethod
	def fetch_subject(cls, subject_id):
		# Fetches a specific subject by subject_id.
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('SELECT subject_id, name, teacher_id FROM subjects WHERE subject_id = ?', (subject_id,))
			subject_data = cursor.fetchone()
			if subject_data:
					return cls(subject_data[0], subject_data[1], subject_data[2])
			return None