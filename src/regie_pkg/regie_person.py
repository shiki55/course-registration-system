"""
This module provides an abstract class representing a user in the REGIE system.
"""

from abc import ABC

from .mongodb import MongoDB
from .text_formatting import insert_newline

class REGIEPerson(ABC):
    """Abstract base class of various users in the system."""
    __mongo_db = MongoDB()

    def __init__(self, name, status, department, email, id):
        self.name = name
        self.status = status
        self.department = department
        self.email = email
        self.id = id

    def change_password(self):
        """
        Change the password of the user's account.

        This method prompts the user to enter their current password and then prompts
        them to enter a new password. If the entered password is correct, the password
        is changed in the database. If the entered password is incorrect, the user has
        the option to try again or cancel the password change.
        """
        class_name = type(self).__name__.lower() # lowercased name of the subclass which calls this method (e.g. "student")
        while True:
            curr_pwd_input = input("Enter your current password: ")
            # verify password
            if self.__mongo_db.verify(id=str(self.id),
                                      curr_password=curr_pwd_input,
                                      collection_name=class_name):
                new_pwd = input("Enter new password: ")
                self.__mongo_db.change_password(id=str(self.id), new_password=new_pwd, collection_name=class_name)
                print("Password change successful.")
                insert_newline()
                break
            try_again = input("Wrong password. Try again [yes/no]?: ")
            if try_again == "yes":
                continue
            elif try_again == "no":
                break
            else:
                print("Invalid input.")
                insert_newline()
                break




