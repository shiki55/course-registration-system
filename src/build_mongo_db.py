"""
Module for building a MongoDB database of student account credentials.

This module imports the necessary functions and establishes a connection to a MongoDB instance,
then drops the credential_db database (if it exists), creates the credential_db database,
creates the student collection in the credential_db database, and inserts the data from the
account_credentials.json file into the student collection.

Note:
- MongoDB must be running in the background.
"""

import json

from regie_pkg.get_mongo_client import get_mongo_client

mongo_client = get_mongo_client()
mongo_client.drop_database('credential_db') # drop credential_db database (if it exists)
credential_db = mongo_client['credential_db'] # credential_db database
student = credential_db['student'] # student collection
with open('../database_files/account_credentials.json', 'r', encoding='utf-8') as f:
    data = json.load(f)
    student.insert_many(data)

# show all documents
# mongo_client = MongoClient()
# credential_db = mongo_client['credential_db'] # credential_db database
# student = credential_db['student'] # student collection
# for document in student.find({}):
#     print(document)

