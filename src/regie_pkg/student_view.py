"""
This module contains classes for viewing a student's information.

This module contains a set of classes for viewing a student's information in
different ways, using a strategy pattern. The `StudentView` class serves as the
base interface for viewing a student's information, and subclasses of `StudentView` define
specific strategies for viewing different kinds of information.
"""
from abc import ABC, abstractmethod

from .mysql_db import MySQLDB
from .text_formatting import underline, bold, insert_newline
from .transcript import Transcript
from .schedule import StudentSchedule

class StudentView(ABC):
    """
    Abstract base class for viewing a student's information.

    This class defines the base interface for viewing a student's information.
    Subclasses should implement the `view` method to define a specific kind of
    information to view.

    Attributes:
    _db (MySQLDB): An instance of the MySQLDB class for interacting with the MySQL database.

    Methods:
    view: Abstract method for viewing a student's information.
          Subclasses should implement this method
    """
    _db = MySQLDB()
    @abstractmethod
    def view(self, student_id):
        pass

class ViewRegisteredCourses(StudentView):
    """
    A class for viewing a student's registered courses and labs.

    This class implements the `view` method of the `StudentView` class to display a
    list of the course sections and labs that a student is registered for.
    """
    def view(self, student_id):
        all_registered = self._db.get_all_registered_course_sections(student_id=student_id) + \
                         self._db.get_all_registered_labs(student_id=student_id)

        if not all_registered:
            print(bold(underline("You are not registered for any course sections or labs.")))
            insert_newline()
            return

        print(bold(underline("Registered course sections and labs:")))
        for enrollable in all_registered:
            course = self._db.get_course(course_id=enrollable.course_id)
            print(bold(f"\t{course.name}: ") + bold(f"registered {enrollable.display_class_name} id {enrollable.id}"))
        insert_newline()
        return

class ViewRestrictions(StudentView):
    """
    A class for viewing a student's restrictions.

    This class implements the `view` method of the `StudentView` class to display
    a list of the restrictions that apply to a student.
    """
    def view(self, student_id):
        student = self._db.get_student(student_id=student_id)
        print(bold("Student Restrictions: ") + f"{student.restrictions}")
        insert_newline()
        return

class ViewTranscript(StudentView):
    """
    A class for viewing a student's transcript.

    This class implements the `view` method of the `StudentView` class to display
    a student's transcript.
    """
    def view(self, student_id):
        Transcript(student_id).view()
        return

class ViewSchedule(StudentView):
    """
    A class for viewing a student's schedule.

    This class implements the `view` method of the `StudentView` class to display
    a week view of a student's schedule.
    """
    def view(self, student_id):
        StudentSchedule(student_id).view_week()
        return