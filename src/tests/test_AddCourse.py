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


class TestAddCourse(unittest.TestCase):
    '''testing all add course functionalities'''
    def setUp(self): # ran before each method w/ prefix "test_"
        self.my_sql_connect = MySQLConnect()
        self.student_id_with_restriction = 1000000
        self.course_section_id_no_approval_req = 89283019
        self.course_id_english = 12121212
        self.non_exist_course_id = 10293810
        self.restriction = 'tuition not paid'
        self.student_id1 = 19090938
        self.course_id_databases = 98928601
        self.course_section_id1_databases = 92930291
        self.course_id_intro_to_comp_sys = 98901928
        self.student_course_grade_id = 293928
        self.my_sql_connect.execute_query(f'''DELETE FROM course_prerequisites WHERE course_id = {self.course_id_databases} AND course_id_prereq = {self.course_id_intro_to_comp_sys}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM student_course_grade WHERE course_id = {self.course_id_english} AND student_id = {self.student_id1}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM course_section WHERE course_section_id = {self.course_section_id_no_approval_req}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM course_section WHERE course_section_id = {self.course_section_id1_databases}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM course WHERE course_id = {self.course_id_english}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM course WHERE course_id = {self.course_id_databases}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM course WHERE course_id = {self.course_id_intro_to_comp_sys}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM student WHERE student_id = {self.student_id1}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM student WHERE student_id = {self.student_id_with_restriction}''', commit=True)
        self.my_sql_connect.execute_query(f'''INSERT INTO student (student_id, name, status, division, department, email, major, restriction) VALUES ({self.student_id_with_restriction}, 'Joe Rogan', 'full-time', 'Division of Physical Sciences', 'Department of Physics', 'rogan@uchicago.edu', 'Physics', '{self.restriction}');''', commit=True)
        self.my_sql_connect.execute_query(f'''INSERT INTO student (student_id, name, status, division, department, email, major, restriction) VALUES ({self.student_id1}, 'Kevin Smith', 'full-time', 'Division of Physical Sciences', 'Department of Physics', 'smith@uchicago.edu', 'Physics', null);''', commit=True)
        self.my_sql_connect.execute_query(f'''INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES ({self.course_id_english}, 'English Grammar and Syntax', 0, 2, 'This course is about grammar and syntax and will invlove a lot of writing.', 'English', 'Department of English Language and Literature');''',commit=True)
        self.my_sql_connect.execute_query(f'''INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES ({self.course_id_intro_to_comp_sys}, 'Introduction to Computer Systems', 0, 1, 'All about computers and how they work.', 'Computer Science', 'Division of Physical Sciences');''', commit=True)
        self.my_sql_connect.execute_query(f'''INSERT INTO course (course_id, name, approval_req, faculty_id, course_desc, subject, division) VALUES ({self.course_id_databases}, 'Databases', 0, 1, 'This course will teach you everything you need to know about databases.', 'Computer Science', 'Division of Physical Sciences');''', commit=True)
        self.my_sql_connect.execute_query(f'''INSERT INTO course_section (course_section_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES ({self.course_section_id_no_approval_req}, 40, 10, 'Tues, Wed', '1:00 PM', '3:00 PM', 'John Crerar Library, Room 110', 2022, 'spring', {self.course_id_english});''',commit=True)
        self.my_sql_connect.execute_query(f'''INSERT INTO course_section (course_section_id, max_reg, curr_reg, days_of_week, start_time, end_time, location, year, quarter, course_id) VALUES ({self.course_section_id1_databases}, 60, 50, 'Mon, Wed, Fri', '2:00 PM', '3:30 PM', 'John Crerar Library, Room 320', 2022, 'winter', {self.course_id_databases});''', commit=True)
        self.my_sql_connect.execute_query(f'''INSERT INTO course_prerequisites (course_id, course_id_prereq) VALUES ({self.course_id_databases}, {self.course_id_intro_to_comp_sys});''', commit=True)
        self.my_sql_connect.execute_query(f'''INSERT INTO student_course_grade (student_course_grade_id, grade, year, quarter, student_id, course_id) VALUES ({self.student_course_grade_id}, 'A', 2021, 'autumn', {self.student_id1}, {self.course_id_english});''', commit=True)


    def tearDown(self):
        self.my_sql_connect.execute_query(f'''DELETE FROM course_prerequisites WHERE course_id = {self.course_id_databases} AND course_id_prereq = {self.course_id_intro_to_comp_sys}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM student_course_grade WHERE course_id = {self.course_id_english} AND student_id = {self.student_id1}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM course_section WHERE course_section_id = {self.course_section_id_no_approval_req}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM course_section WHERE course_section_id = {self.course_section_id1_databases}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM course WHERE course_id = {self.course_id_english}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM course WHERE course_id = {self.course_id_databases}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM course WHERE course_id = {self.course_id_intro_to_comp_sys}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM student WHERE student_id = {self.student_id1}''', commit=True)
        self.my_sql_connect.execute_query(f'''DELETE FROM student WHERE student_id = {self.student_id_with_restriction}''', commit=True)
        return

    @patch('builtins.print')
    def test_add_course_with_student_restrictions(self, mock_print):
        '''adding course when student account has restrictions'''
        course_reg = CourseRegistration()
        student_id = self.student_id_with_restriction
        course_id = self.course_section_id_no_approval_req
        course_reg.add_course(student_id=student_id, course_id=course_id)
        mock_print.assert_called_with("Cannot add course because you have the following restriction(s): tuition not paid")

    @patch('builtins.print')
    def test_add_course_not_exist(self, mock_print):
        '''attempting to add a course which does not exist'''
        course_reg = CourseRegistration()
        student_id = self.student_id1
        course_id = self.non_exist_course_id
        course_reg.add_course(student_id=student_id, course_id=course_id)
        mock_print.assert_called_with(f"Cannot add because {course_id} is not an id for a course section or lab.")

    @patch('builtins.print')
    def test_add_course_prerequisites_not_met(self, mock_print):
        '''attempting to register for a course section for which the student has not met the prerequisites for'''
        course_reg = CourseRegistration()
        student_id = self.student_id1
        course_id = self.course_section_id1_databases
        course_reg.add_course(student_id=student_id, course_id=course_id)
        mock_print.assert_called_with('Course id of courses you need to take before you can register: {98901928}')

  

if __name__ == '__main__':
    unittest.main()
    






