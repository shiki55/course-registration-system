from .REGIEPerson import REGIEPerson

class Student(REGIEPerson):
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
      
    def view(self, StudentView):
        '''strategy pattern (this implementation is sort of like visitor pattern in some ways)'''
        StudentView.view(self.id)
        return 


