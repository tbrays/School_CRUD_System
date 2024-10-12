import unittest
from tools import is_strong_password

class TestPasswordValidation(unittest.TestCase):

	def test_strong_password(self):
		self.assertTrue(is_strong_password('Str0ngP@ssw0rd!'))

	def test_weak_password(self):
		self.assertFalse(is_strong_password('weakpassword'))

if __name__ == '__main__':
		unittest.main()