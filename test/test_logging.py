import unittest
from main import app
import logging

class TestLogging(unittest.TestCase):

	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True

	def test_successful_login_logged(self):
		with self.assertLogs(level='INFO') as cm:  # Capture all logs at INFO level
				self.app.post('/login', data=dict(username='admin', password='admin123'))
		# Check that the log contains the expected message
		self.assertTrue(any('Successful login for user: admin' in message for message in cm.output))

	def test_failed_login_logged(self):
		with self.assertLogs(level='WARNING') as cm:  # Capture all logs at WARNING level
				self.app.post('/login', data=dict(username='wrong', password='wrongpass'))
		# Check that the log contains the expected message
		self.assertTrue(any('Failed login attempt for user: wrong' in message for message in cm.output))

if __name__ == '__main__':
    unittest.main()