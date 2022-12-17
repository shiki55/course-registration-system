
import mysql.connector
from typing import List

class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MySQLConnect(metaclass=Singleton):
    def execute_query(self, query, commit=False, multi=False, database="REGIE_db") -> List[dict]:
        '''Method to execute SQL queries.
           Returns a list of dictionaries where each dictionary represents
           a record (row) in the result-set of the query.
           If no results, then returns an empty list'''
        connection = mysql.connector.connect(
                                    host="localhost",
                                    user="root",
                                    port="3307",
                                    passwd="123abc",
                                    database=database
                                    )
        my_cursor = connection.cursor(dictionary=True)
        if multi:
            # my_cursor.execute(query, multi=True) returns a generator
            # so must iterate through it to process each sql statement
            for _ in my_cursor.execute(query, multi=True): pass
        else:
            my_cursor.execute(query)

        if commit:
            connection.commit()
        res = my_cursor.fetchall()
        my_cursor.close()
        connection.close()
        return res





