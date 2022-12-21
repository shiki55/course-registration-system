"""This module provides a class for interacting with a MongoDB database."""

from regie_pkg.get_mongo_client import get_mongo_client

class MongoDB:
    """Serves as the interface through which domain objects communicate with MongoDB"""
    __mongo_client = get_mongo_client()

    def verify(self, id, curr_password, collection_name) -> bool:
        """Verify whether the given ID and password are correct."""
        password_db = self.__mongo_client['password_db']
        res = password_db[collection_name].find_one({str(id): curr_password})
        if res is None:
            return False
        return True

    def change_password(self, id, new_password, collection_name) -> None:
        """Update the password for the given ID in the database."""
        password_db = self.__mongo_client['password_db']
        res = password_db[collection_name].find_one({str(id): {'$exists': 'true'}})
        mongo_id = res['_id'] # id of post
        password_db[collection_name].update_one({"_id": mongo_id}, {"$set": {str(id): new_password}}, upsert=False) # update post
        return
