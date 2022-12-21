"""This module provides a class for interacting with the MySQL database."""

from typing import List

from .faculty import Faculty
from .MySQLConnect import MySQLConnect
from .Student import Student
from .enrollable import Lab
from .enrollable import CourseSection
from .course import Course
from .course import CompletedCourse

class MySQLDB:
    """
    This class serves as the interface to communicate with the MySQL database.

    The methods in this class create domain layer objects or updates the database.

    Methods:
    - get_student: Retrieve a student object.
    - get_faculty: Retrieve a faculty object.
    - get_lab: Retrieve a lab section object.
    - get_course_section: Retrieve a course section object.
    - get_course: Retrieve a course object.
    - get_all_registered_course_sections: Retrieve a list of course sections
                                          the student is registered for.
    - get_all_pending_registrations: Retrieve a list of course sections the student
                                     is awaiting approval for.
    - get_all_registered_labs: Retrieve a list of labs the student is registered for.
    - is_lab: Check if a given ID corresponds to a lab in the database.
    - is_course_section: Check if a given ID corresponds to a course section in the database.
    - unregister_course: Unregister a student from a course section or lab.
    - register_course: Register a student from a course section or lab.
    - get_completed_courses: Return a list of all courses completed by the student.
    - get_all_prereqs: Get the list of prerequisite courses.
    - get_all_instructors_of_course: Get a list of instructors for a course or lab.
    - get_all_course_sections: Get all course sections for a course.
    - get_all_labs: Get all labs for a course.
    """
    __my_sql_connect = MySQLConnect()

    def get_student(self, student_id) -> Student:
        """
        Retrieve a student object.

        Parameters:
        - student_id (int): The ID of the student to retrieve.

        Returns:
        - Student: The student object corresponding to the given ID.
        """
        student_result = self.__my_sql_connect.execute_query(
                        f'''SELECT * FROM student WHERE student_id = {student_id};'''
                        )
        return Student(
                name=student_result[0]['name'],
                status=student_result[0]['status'],
                department=student_result[0]['department'],
                division=student_result[0]['division'],
                email=student_result[0]['email'],
                id=student_result[0]['student_id'],
                major=student_result[0]['major'],
                restrictions=student_result[0]['restriction'],
            )

    def get_faculty(self, faculty_id) -> Faculty:
        """
        Retrieve a faculty object.

        Parameters:
        - faculty_id (int): The ID of the faculty member to retrieve.

        Returns:
        - Faculty: The faculty object corresponding to the given ID.
        """
        faculty_result = self.__my_sql_connect.execute_query(
                        f'''SELECT * FROM faculty WHERE faculty_id = {faculty_id};'''
                        )
        return Faculty(
                name=faculty_result[0]['name'],
                status=faculty_result[0]['status'],
                email=faculty_result[0]['email'],
                id=faculty_result[0]['faculty_id'],
                title=faculty_result[0]['title'],
            )

    def get_lab(self, lab_id) -> Lab:
        """
        Retrieve a lab section object.

        Parameters:
        - lab_id (int): The ID of the lab to retrieve.

        Returns:
        - Lab: The lab object corresponding to the given ID.
        """
        lab_result = self.__my_sql_connect.execute_query(
                        f'''SELECT * FROM lab WHERE lab_id = {lab_id};'''
                        )

        if not lab_result:
            return None
        lab_result = lab_result[0]

        course = self.get_course(lab_result['course_id'])
        if lab_result:
            return Lab(
                course_id=lab_result['course_id'],
                max_reg=lab_result['max_reg'],
                curr_reg=lab_result['curr_reg'],
                days_of_week=lab_result['days_of_week'],
                start_time=lab_result['start_time'],
                end_time=lab_result['end_time'],
                _id=lab_result['lab_id'],
                location=lab_result['location'],
                year=lab_result['year'],
                quarter=lab_result['quarter'],
                name=course.name,
            )
        return None

    def get_course_section(self, course_section_id) -> CourseSection:
        """
        Retrieve a course section object.

        Parameters:
        - course_section_id (int): The ID of the course section to retrieve.

        Returns:
        - CourseSection: The course section object corresponding to the given ID.
        """
        course_section_result = self.__my_sql_connect.execute_query(
                        f'''SELECT * FROM course_section WHERE course_section_id = {course_section_id};'''
                        )
        if not course_section_result:
            return None
        course_section_result = course_section_result[0]
        course = self.get_course(course_section_result['course_id'])
        if course_section_result:
            return CourseSection(
                course_id=course_section_result['course_id'],
                max_reg=course_section_result['max_reg'],
                curr_reg=course_section_result['curr_reg'],
                days_of_week=course_section_result['days_of_week'],
                start_time=course_section_result['start_time'],
                end_time=course_section_result['end_time'],
                _id=course_section_result['course_section_id'],
                location=course_section_result['location'],
                year=course_section_result['year'],
                quarter=course_section_result['quarter'],
                name=course.name,
            )

    def get_course(self, course_id) -> Course:
        """
        Retrieve a course object.

        Parameters:
        - course_id (int): The ID of the course to retrieve.

        Returns:
        - Course: The course object corresponding to the given ID.
        """
        course_result = self.__my_sql_connect.execute_query(
                        f'''SELECT * FROM course WHERE course_id = {course_id};'''
                        )

        if not course_result:
            return None

        course_result = course_result[0]
        if course_result:
            return Course(
                _id=course_result['course_id'],
                name=course_result['name'],
                approval_req=course_result['approval_req'],
                faculty_id=course_result['faculty_id'],
                desc=course_result['course_desc'],
                subject=course_result['subject'],
                division=course_result['division'],
            )

    def get_all_registered_course_sections(self, student_id) -> List[CourseSection]:
        """
        Retrieve a list of course sections the student is registered for.

        Parameters:
        - student_id (int): The ID of the student.

        Returns:
        - List[CourseSection]: A list of course section objects for which the student is registered.
        """
        registered_course_sections_result = self.__my_sql_connect.execute_query(
                        f'''
                        SELECT *
                        FROM registered_student_section
                        WHERE student_id = {student_id} AND reg_status = 'registered'; '''
                        )

        return [self.get_course_section(record['course_section_id']) for record in registered_course_sections_result ]

    def get_all_pending_registrations(self, student_id) -> List[CourseSection]:
        """
        Retrieve a list of course sections the student is awaiting approval for.

        Parameters:
        - student_id (int): The ID of the student.

        Returns:
        - List[CourseSection]: A list of course section objects for which the student is awaiting approval.
        """
        pending_registrations_result = self.__my_sql_connect.execute_query(
                        f'''
                        SELECT *
                        FROM registered_student_section
                        WHERE student_id = {student_id} AND reg_status = 'awaiting approval'; '''
                        )
        return [self.get_course_section(record['course_section_id']) for record in pending_registrations_result ]

    def get_all_registered_labs(self, student_id) -> List[Lab]:
        """
        Retrieve a list of labs the student is registered for.

        Parameters:
        - student_id (int): The ID of the student.

        Returns:
        - List[Lab]: A list of lab objects for which the student is registered.
        """
        registered_lab_result = self.__my_sql_connect.execute_query(
                        f'''SELECT * FROM registered_student_lab WHERE student_id = {student_id};'''
                        )
        return [self.get_lab(record['lab_id']) for record in registered_lab_result ]

    def is_lab(self, id) -> bool:
        """
        Check if a given ID corresponds to a lab in the database.

        Parameters:
        - id (int): The ID to check.

        Returns:
        - bool: True if the ID corresponds to a lab, False otherwise.
        """
        lab_result = self.__my_sql_connect.execute_query(
                f'''SELECT * FROM lab WHERE lab_id = {id};'''
                )
        if lab_result:
            return True
        return False

    def is_course_section(self, id) -> bool:
        """
        Check if a given ID corresponds to a course section in the database.

        Parameters:
        - id (int): The ID to check.

        Returns:
        - bool: True if the ID corresponds to a course section, False otherwise.
        """
        course_section_result = self.__my_sql_connect.execute_query(
                f'''SELECT * FROM course_section WHERE course_section_id = {id};'''
                )
        if course_section_result:
            return True
        return False

    def unregister_course(self, student_id, course_id) -> None:
        """
        Unregister a student from a course or lab.

        Parameters:
        - student_id (int): The ID of the student.
        - course_id (int): The ID of the course section or lab.
        """
        if self.is_course_section(course_id): # unregistering course section
            self.__my_sql_connect.execute_query(
                                    f'''DELETE FROM registered_student_section WHERE student_id = {student_id}
                                    AND course_section_id = {course_id}
                                    ''',
                                    commit=True
                                    )
            self.__my_sql_connect.execute_query(f'''UPDATE course_section SET curr_reg = curr_reg - 1 WHERE course_section_id = {course_id};''', commit=True)
        else: # unregistering lab
            self.__my_sql_connect.execute_query(
                                    f'''DELETE FROM registered_student_lab WHERE student_id = {student_id}
                                    AND lab_id = {course_id}
                                    ''',
                                    commit=True
                                    )
            self.__my_sql_connect.execute_query(f'''UPDATE lab SET curr_reg = curr_reg - 1 WHERE lab_id = {course_id};''', commit=True)
        return

    def register_course(self, student_id, course_id) -> None:
        """
        Register a student for a course or lab.

        This method will insert and update the database.

        Parameters:
        - student_id (int): The ID of the student.
        - course_id (int): The ID of the course or lab.
        """
        if self.is_course_section(course_id): # course section registration
            self.__my_sql_connect.execute_query(f'''INSERT INTO registered_student_section (course_section_id, student_id, reg_status) VALUES ({course_id}, {student_id}, 'registered');''', commit=True)
            self.__my_sql_connect.execute_query(f'''UPDATE course_section SET curr_reg = curr_reg + 1 WHERE course_section_id = {course_id};''', commit=True)
        else: # lab registration
            self.__my_sql_connect.execute_query(f'''INSERT INTO registered_student_lab (lab_id, student_id) VALUES ({course_id}, {student_id});''', commit=True)
            self.__my_sql_connect.execute_query(f'''UPDATE lab SET curr_reg = curr_reg + 1 WHERE lab_id = {course_id};''', commit=True)

    def get_completed_courses(self, student_id) -> List[CompletedCourse]:
        """
        Return a list of all courses completed by the student.

        Parameters:
        - student_id (int): The ID of the student.

        Returns:
        - List[CompletedCourse]: A list of completed courses.
        """
        result = self.__my_sql_connect.execute_query(
            f'''SELECT *
            FROM student_course_grade
            WHERE student_id = {student_id}'''
            )

        completed_courses = []

        if not result:
            return completed_courses

        for record in result:
            course: Course = self.get_course(record['course_id'])
            completed_courses.append(
                CompletedCourse(
                    _id=course.id,
                    name=course.name,
                    approval_req=course.approval_req,
                    faculty_id=course.faculty_id,
                    desc=course.desc,
                    subject=course.subject,
                    division=course.division,
                    student_id=record['student_id'],
                    grade=record['grade'],
                    year=record['year'],
                    quarter=record['quarter'],
                )
            )
        return completed_courses

    def get_all_prereqs(self, id) -> List[Course]:
        """
        Get the list of prerequisite courses.

        Parameters:
        - id (int): The ID of a course, course section, or lab.

        Returns:
        - List[Course]: A list of prerequisite courses.
        """
        if self.is_course_section(id):
            course_section = self.get_course_section(id)
            id = course_section.course_id # base course id
        elif self.is_lab(id):
            lab = self.get_lab(id)
            id = lab.course_id # base course id

        required_prereqs = self.__my_sql_connect.execute_query(
                         f'''SELECT course_id_prereq FROM course_prerequisites WHERE course_id = {id}'''
                        )

        return [self.get_course(record['course_id_prereq']) for record in required_prereqs]

    def get_all_instructors_of_course(self, id) -> List[Faculty]:
        """
        Get a list of instructors for a course or lab.

        Parameters:
        - id (int): The ID of a course section or lab.

        Returns:
        - List[Faculty]: A list of instructors for the course or lab.
        """
        if self.is_course_section(id=id):
            faculty_id_res = self.__my_sql_connect.execute_query(
                           f'''SELECT faculty_id FROM faculty_course_section WHERE course_section_id = {id}'''
                        )
        else:
            faculty_id_res = self.__my_sql_connect.execute_query(
                           f'''SELECT faculty_id FROM faculty_lab_section WHERE lab_id = {id}'''
                        )
        return [self.get_faculty(record['faculty_id']) for record in faculty_id_res]

    def get_all_course_sections(self, course_id) -> List[CourseSection]:
        """
        Get all course sections for a course.

        Parameters:
        - course_id (int): The ID of the course.

        Returns:
        - List[CourseSection]: A list of course sections.
        """
        course_sections_result = self.__my_sql_connect.execute_query(
                            f'''SELECT * FROM course_section WHERE course_id = {course_id};'''
                            )
        return [self.get_course_section(record['course_section_id']) for record in course_sections_result]

    def get_all_labs(self, course_id) -> List[Lab]:
        """
        Get all labs for a course.

        Parameters:
        - course_id (int): The ID of the course.

        Returns:
        - List[Lab]: A list of labs for the course.
        """
        labs_result = self.__my_sql_connect.execute_query(f'''SELECT * FROM lab WHERE course_id = {course_id};''')
        return [self.get_lab(record['lab_id']) for record in labs_result]



