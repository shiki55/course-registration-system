from regie_pkg.MySQLConnect import MySQLConnect
from time import sleep

'''build mysql db'''


mysql_conn = MySQLConnect()
mysql_conn.execute_query('DROP DATABASE IF EXISTS REGIE_db;', database=None)
mysql_conn.execute_query('CREATE DATABASE REGIE_db;', database=None) 

sleep(1)

# create tables
with open('../sql_files/create_table.sql', encoding='utf-8') as f:
    mysql_conn.execute_query(f.read(), multi=True)

sleep(2)

# populate tables
with open('../sql_files/populate.sql', encoding='utf-8') as f:
    mysql_conn.execute_query(f.read(), multi=True, commit=True)



