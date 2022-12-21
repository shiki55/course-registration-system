from .mysql_db import MySQLDB
from .Student import Student
from .REGIEPerson import REGIEPerson

class REGIEPersonFactory:
    '''factory which returns an instance of a concrete class that inherits from the REGIEPerson abstract class'''
    __db = MySQLDB()
    def get_person(self, id, account_type) -> REGIEPerson:
        if account_type.lower() == "student":
            return self.__create_student(id)

    def __create_student(self, student_id):
        return self.__db.get_student(student_id=student_id)


    # def __create_admin(self, admin_id):
    #     pass
    
    # def __create_faculty(self, admin_id):
    #     pass