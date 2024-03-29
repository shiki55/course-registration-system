"""
Module for viewing a student's transcript.

This module contains the Transcript class, which provides a way
to view a student's transcript, which is a list of courses that the
student has completed.
"""

from typing import List, Tuple

from .mysql_db import MySQLDB
from .student import Student
from .course import CompletedCourse
from .text_formatting import bold, underline, insert_newline
from .pretty_table import PrettyTableWrapper, ALL

class Transcript:
    """
    A class for viewing a student's transcript.

    This class represents a student's transcript, which is a list of courses
    that the student has completed. It provides a `view` method for displaying
    the transcript to the user.

    Attributes:
    student (Student): The student whose transcript is being viewed.
    completed_courses (List[CompletedCourse]): A list of the courses the student has completed.
    __db (MySQLDB): An instance of the MySQLDB class for interacting with the MySQL database.

    Methods:
    view: Display the student's transcript to the user.
    __compare: A private method for sorting the list of completed courses by year and quarter.
    """
    __db = MySQLDB()
    def __init__(self, student_id):
        """
        Initialize a Transcript object.

        Args:
        student_id (int): The ID of the student whose transcript is being viewed.

        Returns:
        None
        """
        self.student: Student = self.__db.get_student(student_id)
        self.completed_courses: CompletedCourse = self.__db.get_completed_courses(student_id)

    def view(self):
        """
        Display the student's transcript to the user.

        This method displays the student's name, status, major, and student ID,
        followed by a list of the courses that the student has completed, sorted by
        year and quarter. If the student has no completed courses, a message is
        displayed indicating that there is no academic history to show.

        Returns:
        None
        """
        if not self.completed_courses:
            print(bold(underline("No academic history to show")))
            insert_newline()

        # sorting based on year (descending) and quarter
        completed_courses_sorted = sorted(self.completed_courses,key=self.__compare, reverse=True)

        print(bold(underline(f"Academic Transcript of {self.student.name}:")))
        print(f"Status: {self.student.status}")
        print(f"Major: {self.student.major}")
        print(f"Student ID: {self.student.id}")
        insert_newline()
        table = self.__create_table(
                    completed_courses=completed_courses_sorted,
                    headers=["course", "grade", "year", "quarter"],
                    )
        print(table)
        insert_newline()

    def __compare(self, course: CompletedCourse) -> Tuple[int, int]:
        """
        A comparator method for sorting the list of completed courses by year and quarter.

        Args:
        course (CompletedCourse): The course to compare.

        Returns:
        Tuple: A tuple containing the year and quarter of the course, in that order.
        """
        quarter_order = {
        "winter": 1,
        "spring": 2,
        "summer": 3,
        "autumn": 4,
        }
        return (course.year, quarter_order[course.quarter])


    def __create_table(self,
                       completed_courses: List[CompletedCourse],
                       headers=List[str]) -> PrettyTableWrapper:
        """
        Create a pretty table for displaying the completed courses.

        Args:
        completed_courses (List[CompletedCourse]): A list of the completed courses to
                                                   include in the table.
        headers (List[str]): A list of the column headers to use for the table.

        Returns:
        PrettyTableWrapper: A PrettyTableWrapper object containing the completed courses data.
        """
        table = PrettyTableWrapper(field_names=headers, hrules=ALL)
        for course in completed_courses:
            table.add_row([course.name, course.grade, course.year, course.quarter])
        return table