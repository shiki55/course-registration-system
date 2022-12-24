import os, sys, inspect
from unittest.mock import patch
##
curr_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
##
from regie_pkg.mysql_connect import MySQLConnect
from regie_pkg.course_registration import CourseRegistration

class TestDropCourse:
    """
    Tests for the drop_course and drop_all methods of CourseRegistration.

    These tests verify that a student can successfully drop a course or all courses
    they are registered for, and that the relevant tables in the database are updated correctly.
    """
    course_reg = CourseRegistration()
    mysql_connect = MySQLConnect()

    @patch('builtins.print')
    def test_drop_course_section_success(self, mock_print):
        """Test that a student can successfully drop a course section."""

        student_id = 1
        course_section_id = 11111114
        self.course_reg.drop_course(student_id=student_id, course_id=course_section_id)

        # check enrollment was decremented by 1
        enrollement_record = self.mysql_connect.execute_query(f'''
                                            SELECT curr_reg
                                            FROM course_section
                                            WHERE course_section_id = {course_section_id}''')
        expected_enrollment = 9
        assert enrollement_record[0]['curr_reg'] == expected_enrollment

        # check record was removed from registered_student_section
        result = self.mysql_connect.execute_query(f'''
                                SELECT *
                                FROM registered_student_section
                                WHERE course_section_id = {course_section_id} AND
                                      student_id = {student_id}''')
        assert result == []

        # test print
        mock_print.assert_called_with("Course drop successful")
        return

    @patch('builtins.print')
    def test_drop_lab_section_success(self, mock_print):
        """Test that a student can successfully drop a lab section."""

        lab_id = 99999999
        student_id = 2
        self.course_reg.drop_course(student_id=student_id, course_id=lab_id)

        # check enrollment was decremented by 1
        enrollement_record = self.mysql_connect.execute_query(f'''SELECT curr_reg FROM lab WHERE lab_id = {lab_id}''')
        expected_enrollment = 13
        assert enrollement_record[0]['curr_reg'] == expected_enrollment

        # check record was removed from registered_student_lab
        result = self.mysql_connect.execute_query(f'''SELECT *
                                                    FROM registered_student_lab
                                                    WHERE lab_id = {lab_id} AND student_id = {student_id}''')
        assert result == []

        # test print
        mock_print.assert_called_with("Course drop successful")
        return

    @patch('builtins.print')
    def test_drop_all_success(self, mock_print):
        """Test that a student can successfully drop all courses they are registered for."""

        student_id = 2
        self.course_reg.drop_all(student_id=student_id)

        # check course section enrollment was decremented by 1
        course_section_id = 11111114
        enrollement_record = self.mysql_connect.execute_query(f'''SELECT curr_reg
                                                FROM course_section
                                                WHERE course_section_id = {course_section_id}''')
        expected_enrollment = 9
        assert enrollement_record[0]['curr_reg'] == expected_enrollment

        # check lab section enrollment was decremented by 1
        lab_id = 99999999
        enrollement_record = self.mysql_connect.execute_query(f'''SELECT curr_reg
                                                                  FROM lab
                                                                  WHERE lab_id = {lab_id}''')
        expected_enrollment = 13

        assert enrollement_record[0]['curr_reg'] == expected_enrollment

        # check record was removed from registered_student_section and registered_student_lab
        course_section_reg = self.mysql_connect.execute_query(f'''SELECT *
                                                            FROM registered_student_section
                                                            WHERE student_id = {student_id}''')
        lab_reg = self.mysql_connect.execute_query(f'''SELECT *
                                                    FROM registered_student_lab
                                                    WHERE student_id = {student_id}''')
        assert course_section_reg == []
        assert lab_reg == []

        # test print
        mock_print.assert_called_with("Dropped all courses")
        return
        