from pymongo import MongoClient

class MongoDB:
    '''serves as an interface for classes/objects to communicate w/ MongoDB'''

    __password_db = MongoClient()['password_db']

    def verify(self, id, curr_password, collection_name) -> bool:
        '''verifies whether id (student_id, faculty_id, admin_id) and password is correct'''
        res = self.__password_db[collection_name].find_one({str(id): curr_password})
        if res is None:
            return False
        return True
    
    def change_password(self, id, new_password, collection_name) -> None:
        '''updates mongodb w/ new password for the given id (student_id, faculty_id, admin_id)'''
        res = self.__password_db[collection_name].find_one({str(id): {'$exists': 'true'}})
        mongo_id = res['_id'] # id of post
        self.__password_db[collection_name].update_one({"_id": mongo_id}, {"$set": {str(id): new_password}}, upsert=False) # update post
        return
