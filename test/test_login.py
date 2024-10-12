import unittest
from main import app

class TestLoginRoute(unittest.TestCase):

	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True

	def test_valid_login(self):
		response = self.app.post('/login', data=dict(username='admin', password='admin123'))
		self.assertEqual(response.status_code, 302)  # Redirects to dashboard

	def test_invalid_login(self):
		response = self.app.post('/login', data=dict(username='wrong', password='wrongpass'))
		self.assertIn(b'Invalid username or password', response.data)

if __name__ == '__main__':
		unittest.main()
