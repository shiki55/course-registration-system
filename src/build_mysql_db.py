from regie_pkg.MySQLConnect import MySQLConnect
import mysql.connector
from time import sleep

'''build mysql db'''

db = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="123abc$$$"
)
my_cursor = db.cursor()
my_cursor.execute('DROP DATABASE IF EXISTS REGIE_db;')
my_cursor.execute('CREATE DATABASE REGIE_db;') 

sleep(1)

# create tables
my_sql_conn = MySQLConnect()
with open('../database_files/create_table.sql') as f:
    my_sql_conn.execute_query(f.read())

sleep(2)

# populate tables
my_sql_conn = MySQLConnect()
with open('../database_files/populate.sql') as f:
    insert_queries = [q for q in f.read().split(";") if len(q.strip()) > 0]
    for insert_query in insert_queries:
        my_sql_conn.execute_query(insert_query + ';', commit=True)
