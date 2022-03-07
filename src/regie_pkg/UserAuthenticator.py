from .MongoDB import MongoDB

# use MongoDB
class UserAuthenticator:
    '''authenticates login credentials'''
    __mongo_db = MongoDB()

    def authenticate(self, id, password, account_type: str) -> bool:
        if self.__mongo_db.verify(id, curr_password=password, collection_name=account_type.lower()):
            print("id and password have been authenticated.")
            return True
        False
