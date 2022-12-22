import os, sys, inspect
from unittest import TestCase, mock
import unittest
##
curr_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
##
from regie_pkg.student import Student
from regie_pkg.get_mongo_client import get_mongo_client


class TestChangePassword(TestCase):
    def setUp(self): # ran before each method w/ prefix "test_"
        self.mongo_client = get_mongo_client()
        self.student_id = '100'
        self.initial_password = 'password123'
        self.mongo_client.password_db.student.insert_one({self.student_id: self.initial_password})
        self.student_obj = Student(id=int(self.student_id))
        return

    def tearDown(self):
        res = self.mongo_client.password_db.student.find_one({self.student_id: {'$exists': 'true'}})
        self.mongo_client.password_db.student.delete_one(res)
        return

    @mock.patch('regie_pkg.regie_person.input', create=True)
    def test_change_password_student(self, mock_input):
        new_password = 'new_password'
        mock_input.side_effect = [self.initial_password, new_password] # mock inputs
        self.student_obj.change_password()
        res = self.mongo_client.password_db.student.find_one({self.student_id: {'$exists': 'true'}})
        actual_password = res[self.student_id]
        self.assertEqual(actual_password, new_password)


if __name__ == '__main__':
    unittest.main()