"""
This module provides a REGIEPersonFactory class which is responsible for
creating REGIEPerson objects. The REGIEPerson objects are either Student
objects or Faculty objects. The REGIEPersonFactory class has a get_person
method which returns a REGIEPerson object based on the given id and account type.
"""
from .mysql_db import MySQLDB
from .regie_person import REGIEPerson

class REGIEPersonFactory:
    """
    Factory class which returns an object representing a user.
    """
    __db = MySQLDB()
    def get_person(self, id, account_type) -> REGIEPerson:
        """Return a user of the REGIE system"""
        if account_type.lower() == "student":
            return self.__db.get_student(student_id=id)

