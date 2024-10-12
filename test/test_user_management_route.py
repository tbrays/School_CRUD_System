import unittest
from main import app

class TestManageTimetableRoute(unittest.TestCase):

	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True

	def test_admin_access_create_entry(self):
		# Simulate admin user login and timetable creation
		with self.app.session_transaction() as sess:
				sess['role'] = 'admin'
		response = self.app.post('/manage_timetable', data=dict(user_id=1, subject_id=1, day_of_week='Monday', start_time='10:00', end_time='11:00'))
		self.assertEqual(response.status_code, 302)  # Redirects after timetable creation

	def test_admin_access_delete_entry(self):
		with self.app.session_transaction() as sess:
				sess['role'] = 'admin'
		response = self.app.post('/manage_timetable', data=dict(entry_id=1))
		self.assertEqual(response.status_code, 302)

if __name__ == '__main__':
		unittest.main()
