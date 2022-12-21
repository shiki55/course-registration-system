from abc import ABC
from .MongoDB import MongoDB

class REGIEPerson(ABC):
    '''abstract base class of people (students, faculty, admin)'''
    __mongo_db = MongoDB()

    def __init__(self, name, status, department, email, id):
        self.name = name
        self.status = status
        self.department = department
        self.email = email
        self.id = id

    def change_password(self): # protected method
        class_name = type(self).__name__.lower() # name of the subclass which calls this method
        while True:
            curr_pwd_input = input("Enter your current password: ")
            if self.__mongo_db.verify(id=str(self.id), curr_password=curr_pwd_input, collection_name=class_name): # check if user input password is correct
                new_pwd = input("Enter new password: ")
                self.__mongo_db.change_password(id=str(self.id), new_password=new_pwd, collection_name=class_name)
                print("Password change successful.")
                print("")
                break
            try_again = input("Wrong password. Try again [yes/no]?: ") 
            if try_again == "yes":
                continue
            elif try_again == "no":
                break
            else:
                print("Invalid input.")
                print("")
                break




