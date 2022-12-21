"""
This module has classes which implements the processes for
registering for courses which require approval and student overloads.
"""

from abc import ABC, abstractmethod
from .email import Email
from .notification_service import NotificationService
from .mysql_db import MySQLDB

class IApprovalRequired(ABC):
    """
    Interface for handlers which deal with
    registering for courses that require approval.
    """
    @abstractmethod
    def ApprovalRequiredHandler(self, student_id, course_id):
        """Handle the approval required process."""

class IStudentOverload(ABC):
    """
    Interface for handlers which deal with
    students attempting to register for more courses
    than typically allowed (overloading).
    """
    @abstractmethod
    def StudentOverloadHandler(self, student_id):
        """Handle the registration overload process."""

class RegistrationApproval(IApprovalRequired, IStudentOverload):
    """
    Implements the necessary procedures when approval/permission is required for
    the ApprovalRequiredHandler and StudentOverloadHandler classes.
    """

    __db = MySQLDB()
    notification_service = NotificationService()
    email = Email
    def ApprovalRequiredHandler(self, student_id, course_id):
        """
        Approval actions for ApprovalRequiredHandler
           1. Find student email address
           2. Find instructor email address
           3. Send email
        """
        print("Instructor approval is required to register for this course. Approval request email will be sent.")
        student = self.__db.get_student(student_id=student_id)
        instructors = self.__db.get_all_instructors_of_course(id=course_id)
        instructor = instructors[0]

        self.notification_service.notif_strategy = self.email(sender=student.email, to=instructor.email,
                                                       subject='course registration approval request',
                                                       body='I am requesting approval to register for your approval required course.')
        self.notification_service.send_notification()
        return

    def StudentOverloadHandler(self, student_id):
        """
        Approval actions for StudentOverloadHandler
           1. Find student email address
           2. Find student status ('part-time' or 'full-time')
           3. Send email
        """
        student = self.__db.get_student(student_id=student_id)
        print(f"As a {student.status} student adding this course requires overload approval. Approval request email will be sent.")
        self.notification_service.notif_strategy = self.email(sender=student.email, to='department_chair@uchicago.edu',
                                                   subject='overload request', body='I am requesting approval for overload registration' ,
                                                   cc='academic_advisor@uchicago.edu')
        self.notification_service.send_notification()
        return