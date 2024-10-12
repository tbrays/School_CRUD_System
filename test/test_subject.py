import unittest
from subject import Subject

class TestSubjectManagement(unittest.TestCase):

	def test_create_subject(self):
		subject = Subject.create_subject('Mathematics')
		self.assertIsNotNone(subject)
		self.assertEqual(subject.name, 'Mathematics')

	def test_delete_subject(self):
		subject = Subject.create_subject('Mathematics')
		Subject.delete_subject(subject.subject_id)
		self.assertIsNone(Subject.fetch_subject(subject.subject_id))

if __name__ == '__main__':
		unittest.main()
