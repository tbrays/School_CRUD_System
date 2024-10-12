import unittest
from timetable import Timetable

class TestTimetableManagement(unittest.TestCase):

	def test_create_entry(self):
		entry = Timetable.create_timetable_entry(1, 1, 'Monday', '09:00', '10:00')
		self.assertIsNotNone(entry)
		self.assertEqual(entry.day_of_week, 'Monday')

	def test_view_entry(self):
		# This assumes user_id 1 has at least one timetable entry.
		entries = Timetable.get_timetable(1)
		self.assertGreater(len(entries), 0)

	def test_delete_entry(self):
		# Create a new timetable entry to delete it later
		entry = Timetable.create_timetable_entry(1, 1, 'Monday', '09:00', '10:00')
		Timetable.delete_timetable_entry(entry.entry_id)  
		self.assertIsNone(Timetable.fetch_timetable_entry(entry.entry_id))

if __name__ == '__main__':
    unittest.main()
