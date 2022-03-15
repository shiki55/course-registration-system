import os, sys, inspect
from unittest.mock import patch
import unittest
##
curr_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
##
from regie_pkg.MySQLConnect import MySQLConnect
from regie_pkg.CourseRegistration import CourseRegistration

class TestDropCourse(unittest.TestCase):
    '''testing all drop course functionalities'''
    def setUp(self): # ran before each method w/ prefix "test_"
        self.my_sql_connect = MySQLConnect()
        self.student_id = 10000
        self.dropping_lab_id = 26738986
        self.dropping_course_section_id = 92794684
        # including delete commands in setUp is precautionary
        self.my_sql_connect.execute_query(f'''DELETE FROM registered_student_lab WHERE student_id = {self.student_id}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM registered_student_section WHERE student_id = {self.student_id}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM course_section WHERE course_section_id = {self.dropping_course_section_id}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM student WHERE student_id = {self.student_id}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM lab WHERE lab_id = {self.dropping_lab_id}''', commit=True)
        self.my_sql_connect.execute_query(f'''INSERT INTO student (student_id, name, status, division, department, email, major, restriction) VALUES 
                                              ({self.student_id}, 'James Bond', 'full-time', 'Division of Physical Sciences', 'Department of Mathematics', 'bond@uchicago.edu', 'mathematics', null);'''
                                              ,commit=True)            
        self.my_sql_connect.execute_query(f'''INSERT INTO lab (lab_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES 
                                              ({self.dropping_lab_id}, 30, 15, 'Fri', '5:00 PM', '6:00 PM', 'Ryerson Laboratory, Room 115', 2022, 'spring', 11111111);'''
                                              ,commit=True)
        self.my_sql_connect.execute_query(f'''INSERT INTO course_section (course_section_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES 
                                              ({self.dropping_course_section_id}, 50, 20, 'Mon, Wed, Fri', '5:00 PM', '6:30 PM', 'John Crerar Library, Room 320', 2022, 'spring', 11111111);'''
                                              ,commit=True)
        self.my_sql_connect.execute_query(f'''INSERT INTO registered_student_lab (lab_id, student_id) VALUES ({self.dropping_lab_id}, {self.student_id});'''
                                              ,commit=True)
        self.my_sql_connect.execute_query(f'''INSERT INTO registered_student_section (course_section_id, student_id, reg_status) VALUES ({self.dropping_course_section_id}, {self.student_id}, 'registered');'''
                                              ,commit=True)

    def tearDown(self):
        self.my_sql_connect.execute_query(f'''DELETE FROM registered_student_lab WHERE student_id = {self.student_id}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM registered_student_section WHERE student_id = {self.student_id}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM course_section WHERE course_section_id = {self.dropping_course_section_id}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM student WHERE student_id = {self.student_id}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM lab WHERE lab_id = {self.dropping_lab_id}''', commit=True)
        return

    @patch('builtins.print')
    def test_drop_course_section(self, mock_print):
        '''dropping course section registration'''
        course_reg = CourseRegistration()
        course_reg.drop_course(student_id=self.student_id, course_id=self.dropping_course_section_id)

        # check enrollment was decremented by 1
        enrollement_record = self.my_sql_connect.execute_query(f'''SELECT curr_reg FROM course_section WHERE course_section_id = {self.dropping_course_section_id}''')
        expected_enrollment = 19
        self.assertEqual(enrollement_record[0]['curr_reg'], expected_enrollment)

        # check record was removed from registered_student_section
        res = self.my_sql_connect.execute_query(f'''SELECT * FROM registered_student_section WHERE course_section_id = {self.dropping_course_section_id}''')
        self.assertEqual(res, [])
        
        # test print 
        mock_print.assert_called_with("Course drop successful")
        return 

    @patch('builtins.print')
    def test_drop_course_lab(self, mock_print):
        '''dropping lab registration'''
        course_reg = CourseRegistration()
        course_reg.drop_course(student_id=self.student_id, course_id=self.dropping_lab_id)

        # check enrollment was decremented by 1
        enrollement_record = self.my_sql_connect.execute_query(f'''SELECT curr_reg FROM lab WHERE lab_id = {self.dropping_lab_id}''')
        expected_enrollment = 14
        self.assertEqual(enrollement_record[0]['curr_reg'], expected_enrollment)

        # check record was removed from registered_student_lab
        res = self.my_sql_connect.execute_query(f'''SELECT * FROM registered_student_lab WHERE lab_id = {self.dropping_lab_id}''')
        self.assertEqual(res, [])

        # test print
        mock_print.assert_called_with("Course drop successful")
        return 

    @patch('builtins.print')
    def test_drop_all(self, mock_print):
        '''drop all registrations'''
        course_reg = CourseRegistration()
        course_reg.drop_all(student_id=self.student_id)
        course_section_reg = self.my_sql_connect.execute_query(f'''SELECT * FROM registered_student_section WHERE student_id = {self.student_id}''')
        lab_reg = self.my_sql_connect.execute_query(f'''SELECT * FROM registered_student_lab WHERE student_id = {self.student_id}''')

        # check enrollment was decremented by 1
        enrollement_record = self.my_sql_connect.execute_query(f'''SELECT curr_reg FROM course_section WHERE course_section_id = {self.dropping_course_section_id}''')
        expected_enrollment = 19
        self.assertEqual(enrollement_record[0]['curr_reg'], expected_enrollment)

        # check enrollment was decremented by 1
        enrollement_record = self.my_sql_connect.execute_query(f'''SELECT curr_reg FROM lab WHERE lab_id = {self.dropping_lab_id}''')
        expected_enrollment = 14
        self.assertEqual(enrollement_record[0]['curr_reg'], expected_enrollment)

        # check record was removed from registered_student_section and registered_student_lab
        self.assertEqual(course_section_reg, [])
        self.assertEqual(lab_reg, [])

        # test print
        mock_print.assert_called_with("Dropped all courses")
        return 



if __name__ == '__main__':
    unittest.main()
    

