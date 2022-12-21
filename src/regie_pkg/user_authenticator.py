"""
This module contains a class to authenticate
the user login credentials.
"""

from .mongodb import MongoDB

class UserAuthenticator:
    """
    A class for authenticating user login credentials.

    This class contains the authenticate method, which verifies that
    the given id and password match the credentials stored in the MongoDB
    database for the specified account_type.

    Attributes:
    __mongo_db (MongoDB): An instance of the MongoDB class for interacting with the MongoDB database.

    Methods:
    authenticate(id, password, account_type) -> bool: Verify that the given id and password match
                                                      the credentials stored in the MongoDB database for
                                                      the specified account_type.
                                                      Returns True if the credentials are valid, False otherwise.
    """
    __mongo_db = MongoDB()

    def authenticate(self, id, password, account_type: str) -> bool:
        """Authenticate login credentials."""
        if self.__mongo_db.verify(id, curr_password=password, collection_name=account_type.lower()):
            print("id and password have been authenticated.")
            return True
        return False
