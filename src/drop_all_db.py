from regie_pkg.MySQLConnect import MySQLConnect
from pymongo import MongoClient

# dropping all databases

my_sql_conn = MySQLConnect()
my_sql_conn.execute_query('DROP DATABASE IF EXISTS REGIE_db;')


mongo_client = MongoClient()
mongo_client.drop_database('password_db') 