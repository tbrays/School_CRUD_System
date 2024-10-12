import re
import sqlite3


class GlobalSettings:
	@classmethod
	def get_security_setting(cls):
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('SELECT security_enabled FROM global_settings WHERE id = 1')
			setting = cursor.fetchone()
			return setting[0] if setting else True 

	@classmethod
	def update_security_setting(cls, security_enabled):
		with sqlite3.connect('database.db') as db:
			cursor = db.cursor()
			cursor.execute('UPDATE global_settings SET security_enabled = ? WHERE id = 1', (security_enabled,))
			db.commit()


def is_strong_password(password):
	# Define the criteria for a strong password
	if (len(password) < 8 or
		not re.search(r"[a-z]", password) or  # At least one lowercase letter
		not re.search(r"[A-Z]", password) or  # At least one uppercase letter
		not re.search(r"[0-9]", password) or  # At least one digit
		not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):  # At least one special character
		return False
	return True