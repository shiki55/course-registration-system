"""
Drop the REGIE_db MySQL database and the password_db MongoDB database.
"""

from regie_pkg.mysql_connect import MySQLConnect
from regie_pkg.get_mongo_client import get_mongo_client

MySQLConnect.set_database(None)
my_sql_conn = MySQLConnect()
my_sql_conn.execute_query('DROP DATABASE IF EXISTS REGIE_db;')

mongo_client = get_mongo_client()
mongo_client.drop_database('password_db')
