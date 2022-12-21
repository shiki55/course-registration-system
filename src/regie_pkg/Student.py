"""This module contains the Student class."""

from .regie_person import REGIEPerson
from .StudentView import StudentView

class Student(REGIEPerson):
    """
    A class representing a student in the registration system.

    Inherits from the REGIEPerson class and adds additional attributes specific to students,
    such as major, division, and restrictions.
    """
    def __init__(self,
                name=None,
                status=None,
                department=None,
                division=None,
                email=None,
                id=None,
                major=None,
                restrictions=None,
                ):
        super().__init__(name, status, department, email, id)
        self.major = major
        self.division = division
        self.restrictions=restrictions

    def view(self, student_view: StudentView):
        """
        Apply a student view strategy to view the student's information (e.g. transcript, schedule, etc).

        This method uses the strategy pattern to view different kinds of student information.

        Args:
        student_view (StudentView): A class that defines a view strategy for the student.

        Returns:
        None
        """
        student_view.view(self.id)
        return
