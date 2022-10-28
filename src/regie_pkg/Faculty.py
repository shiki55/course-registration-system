from .REGIEPerson import REGIEPerson

class Faculty(REGIEPerson):
    def __init__(self, 
                name=None, 
                status=None, 
                email=None, 
                id=None, 
                title=None,
                ):
        super().__init__(name=name, 
                        status=status, 
                        department="", 
                        email=email, 
                        id=id,
                        )
        self.title = title