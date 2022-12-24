import os, sys, inspect
from unittest.mock import patch
##
curr_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
##
from regie_pkg.course_registration import CourseRegistration
from regie_pkg.mysql_connect import MySQLConnect

class TestAddCourse:
    """Test suite for the add_course method of the CourseRegistration class."""

    course_reg = CourseRegistration()
    mysql_connect = MySQLConnect()

    @patch('builtins.print')
    def test_add_course_with_student_restrictions(self, mock_print):
        """Prevent registering for a course when student account has restrictions"""
        student_id = 2
        course_section_id = 11111115
        self.course_reg.add_course(student_id=student_id, course_id=course_section_id)
        mock_print.assert_called_with("Cannot add course because you have the following restriction(s): tuition not paid")

    @patch('builtins.print')
    def test_add_course_not_exist(self, mock_print):
        """Prevent registeration for a course which does not exist"""
        student_id = 1
        course_section_id = 11092906
        self.course_reg.add_course(student_id=student_id, course_id=course_section_id)
        mock_print.assert_called_with(f"Cannot add because {course_section_id} is not an id for a course section or lab.")

    @patch('builtins.print')
    def test_add_course_prerequisites_not_met(self, mock_print):
        """Prevent registration for a course for which the prerequisites have not been met."""
        course_reg = CourseRegistration()
        student_id = 3
        course_section_id = 11111116
        course_reg.add_course(student_id=student_id, course_id=course_section_id)
        mock_print.assert_called_with("\033[1m\tCourse Name: \033[0mIntroduction to Computer Systems")

    @patch('builtins.print')
    def test_add_course_already_registered(self, mock_print):
        """Prevent registration for a course for which a student is already registered for."""
        course_reg = CourseRegistration()
        student_id = 1
        course_section_id = 11111114
        course_reg.add_course(student_id=student_id, course_id=course_section_id)
        mock_print.assert_called_with(f"Cannot add because you are already registered for a course section or lab with id {course_section_id}")

    @patch('builtins.print')
    def test_add_course_section(self, mock_print):
        """successful registration to a section of a course"""
        course_reg = CourseRegistration()
        student_id = 1
        course_section_id = 11111121
        course_reg.add_course(student_id=student_id, course_id=course_section_id)

        # check record was inserted into registered_student_section
        actual_record = self.mysql_connect.execute_query(f"""SELECT *
                                                             FROM registered_student_section
                                                             WHERE course_section_id = {course_section_id} AND
                                                                   student_id = {student_id}""")
        expected_record = {"course_section_id": course_section_id,
                            "student_id": student_id,
                            "reg_status": "registered"}

        assert actual_record[0] == expected_record

        # check enrollment was incremented by 1
        enrollement_record = self.mysql_connect.execute_query(f"""SELECT curr_reg
                                                                  FROM course_section
                                                                  WHERE course_section_id = {course_section_id}""")
        expected_enrollment = 22
        assert enrollement_record[0]['curr_reg'] == expected_enrollment

        # success print statement
        mock_print.assert_called_with("Successfully registered for the requested course section.")










