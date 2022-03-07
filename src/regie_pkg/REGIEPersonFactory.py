from .DB import DB
from .Student import Student
from .REGIEPerson import REGIEPerson

class REGIEPersonFactory:
    '''factory which returns an instance of a concrete class that inherits from the REGIEPerson abstract class'''
    __db = DB()
    def get_person(self, id, account_type) -> REGIEPerson:
        if account_type.lower() == "student":
            return self.__create_student(id)

    def __create_student(self, student_id):
        student_res = self.__db.get_student_profile(student_id=student_id)
        return Student(
                        name=student_res['name'], 
                        status=student_res['status'], 
                        department=student_res['department'], 
                        division=student_res['division'], 
                        email=student_res['email'], 
                        id=student_res['student_id'], 
                        major=student_res['student_id']
                    )


    # def __create_admin(self, admin_id):
    #     pass
    
    # def __create_faculty(self, admin_id):
    #     pass