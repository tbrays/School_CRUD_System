import unittest
from user import User

class TestUserManagement(unittest.TestCase):
    
	def test_create_user(self):
		user = User.create_user('testuser', 'testpassword', 'test@example.com')
		self.assertIsNotNone(user)
		self.assertEqual(user.username, 'testuser')

	def test_delete_user(self):
		user = User.create_user('testuser', 'testpassword', 'test@example.com')
		User.delete_user(user.user_id)
		self.assertIsNone(User.fetch_user(user.user_id))

if __name__ == '__main__':
    unittest.main()

