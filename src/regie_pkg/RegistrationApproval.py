from abc import ABC, abstractmethod
from .Email import Email
from .NotificationService import NotificationService
from .DB import DB

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

    __db = DB()
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
        student_result = self.__db.get_student_profile(student_id=student_id)
        ids_of_instructors = self.__db.get_all_instructors_of_course(id=course_id)
        instructor_id = ids_of_instructors[0]
        instructor_result = self.__db.get_faculty_profile(faculty_id=instructor_id)

        self.notification_service.notif_strategy = self.Email(sender=student_result['email'], to=instructor_result['email'], 
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
        student_result = self.__db.get_student_profile(student_id=student_id)
        student_status = student_result['status']
        student_email = student_result['email']
        print(f"As a {student_status} student adding this course requires overload approval. Approval request email will be sent.")
        self.notification_service.notif_strategy = self.Email(sender=student_email, to='department_chair@uchicago.edu', 
                                                   subject='overload request', body='I am requesting approval for overload registration' , 
                                                   cc='academic_advisor@uchicago.edu')
        self.notification_service.send_notification()
        return