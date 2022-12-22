"""
This module provides a class for connecting to a MySQL database and executing SQL queries.

The MySQLConnect class is implemented as a singleton to ensure that there is only one instance
of it at any given time so that multiple connections to the database are not created.
"""

import mysql.connector

from typing import List

class Singleton(type):
    """Singleton design pattern"""
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class MySQLConnect(metaclass=Singleton):
    def execute_query(self, query, commit=False, multi=False, database="REGIE_db") -> List[dict]:
        """
        Execute a SQL query on the database.

        Parameters:
        - query (str): The SQL query to execute.
        - commit (bool): Whether or not to commit the changes made by the query. Defaults to False.
        - multi (bool): Whether or not the query is a multi-statement query. Defaults to False.
        - database (str): The name of the database to connect to. Defaults to "REGIE_db".

        Returns:
        - List[dict]: A list of dictionaries representing the records (rows) in the result set of the query.
        """
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
