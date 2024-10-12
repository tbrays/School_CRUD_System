import sqlite3

class Timetable:
	# Class for managing timetable entries for users.

	def __init__(self, entry_id, user_id, subject_id, day_of_week, start_time, end_time):
		self.entry_id = entry_id  # Unique identifier for the timetable entry
		self.user_id = user_id  # Foreign key to User
		self.subject_id = subject_id  # Foreign key to Subject
		self.day_of_week = day_of_week  # Day of the week
		self.start_time = start_time  # Class start time
		self.end_time = end_time  # Class end time

	@classmethod
	def create_timetable_entry(cls, user_id, subject_id, day_of_week, start_time, end_time):
		# Creates a timetable entry for a user.
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('''
				INSERT INTO timetable (user_id, subject_id, day_of_week, start_time, end_time)
				VALUES (?, ?, ?, ?, ?)
			''', (user_id, subject_id, day_of_week, start_time, end_time))
			db.commit()
			entry_id = cursor.lastrowid
		return cls(entry_id, user_id, subject_id, day_of_week, start_time, end_time)

	@classmethod
	def get_timetable(cls, user_id):
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('''
				SELECT t.timetable_id, t.day_of_week, t.start_time, t.end_time, s.name
				FROM timetable t
				JOIN subjects s ON t.subject_id = s.subject_id
				WHERE t.user_id = ?
				ORDER BY t.day_of_week, t.start_time
			''', (user_id,))
			rows = cursor.fetchall()
		return [cls(row[0], user_id, row[4], row[1], row[2], row[3]) for row in rows]

	@classmethod
	def delete_timetable_entry(cls, entry_id):
		# Deletes a timetable entry by entry_id.
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('DELETE FROM timetable WHERE timetable_id = ?', (entry_id,))
			db.commit()

	@classmethod
	def fetch_timetable_entry(cls, entry_id):
		# Fetches a specific timetable entry by entry_id.
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('SELECT * FROM timetable WHERE timetable_id = ?', (entry_id,))
			row = cursor.fetchone()
			if row:
					return cls(row[0], row[1], row[2], row[3], row[4], row[5])
		return None
