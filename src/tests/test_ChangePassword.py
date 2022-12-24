import os, sys, inspect
from unittest import mock
##
curr_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
##
from regie_pkg.student import Student
from regie_pkg.get_mongo_client import get_mongo_client


class TestChangePassword:
    """A class for testing the change_password method of abstract class REGIEPerson"""

    mongo_client = get_mongo_client()
    student = Student(id=1)

    @mock.patch('regie_pkg.regie_person.input', create=True)
    def test_change_password_student_success(self, mock_input):
        """Test the change_password method with a successful password change."""
        
        original_password = 'pass123'
        new_password = 'new_password'
        mock_input.side_effect = [original_password, new_password] # mock input

        self.student.change_password()
        student_id = str(self.student.id)
        result = self.mongo_client.credential_db_test.student.find_one({student_id: {'$exists': 'true'}})
        print(result)
        actual_password = result[student_id]
        assert actual_password == new_password
