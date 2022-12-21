"""This module contains the `Faculty` class."""

from .regie_person import REGIEPerson

class Faculty(REGIEPerson):
    """This class represents a faculty member."""
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