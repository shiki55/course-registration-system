# make sure mongodb is running in the background

'''build mongodb'''

from pymongo import MongoClient

username = 'root'
password = '123abc'
host = 'localhost'
port = 27017
mongo_client = MongoClient(f'mongodb://{username}:{password}@{host}:{port}/')

mongo_client.drop_database('password_db') # drop password_db database
password_db = mongo_client['password_db'] # password_db database
student = password_db['student'] # student collection
# student id, password pair
student1 = {'1': 'pass123'}
student2 = {'2': 'pass123'}
student3 = {'3': 'pass123'}
student.insert_many([
                    student1,
                    student2,
                    student3,
                ])




# show all documents
# mongo_client = MongoClient()
# password_db = mongo_client['password_db'] # password_db database
# student = password_db['student'] # student collection
# for document in student.find({}):
#     print(document)

