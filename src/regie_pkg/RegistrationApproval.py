from abc import ABC, abstractmethod
from .Email import Email
from .NotificationService import NotificationService
from .mysql_db import MySQLDB

class IApprovalRequired(ABC):
    @abstractmethod
    def ApprovalRequiredHandler(self, student_id, course_id):
        pass

class IStudentOverload(ABC):
    @abstractmethod
    def StudentOverloadHandler(self, student_id):
        pass

class RegistrationApproval(IApprovalRequired, IStudentOverload):
    '''Implements the necessary procedures when approval/permission is required for 
       the ApprovalRequiredHandler and StudentOverloadHandler classes'''

    __db = MySQLDB()
    notification_service = NotificationService()
    Email = Email
    def ApprovalRequiredHandler(self, student_id, course_id):
        '''approval actions for ApprovalRequiredHandler 
           1. find student email address
           2. find instructor email address
           3. send email
        *Assuming one instructor per course section or lab
        '''
        print("Instructor approval is required to register for this course. Approval request email will be sent.")
        student = self.__db.get_student(student_id=student_id)
        instructors = self.__db.get_all_instructors_of_course(id=course_id)
        instructor = instructors[0]

        self.notification_service.notif_strategy = self.Email(sender=student.email, to=instructor.email, 
                                                       subject='course registration approval request', 
                                                       body='I am requesting approval to register for your approval required course.')
        self.notification_service.send_notification()
        return  

    def StudentOverloadHandler(self, student_id):
        '''approval actions for StudentOverloadHandler
           1. find student email address
           2. find student status ('part-time' or 'full-time')
           3. send email
        '''
        student = self.__db.get_student(student_id=student_id)
        print(f"As a {student.status} student adding this course requires overload approval. Approval request email will be sent.")
        self.notification_service.notif_strategy = self.Email(sender=student.email, to='department_chair@uchicago.edu', 
                                                   subject='overload request', body='I am requesting approval for overload registration' , 
                                                   cc='academic_advisor@uchicago.edu')
        self.notification_service.send_notification()
        return