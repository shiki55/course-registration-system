"""
Build a MySQL database for the REGIE application.

This script does the following:
1. Connects to a MySQL server using the MySQLConnect class from the regie_pkg package.
2. Drops the REGIE_db database if it exists.
3. Creates the REGIE_db database.
4. Executes the SQL statements in the 'create_table.sql' file to
   create the tables in the REGIE_db database.
5. Executes the SQL statements in the 'populate.sql' file to populate the
   tables in the REGIE_db database.

Note:
- The MySQL server must be running and accessible.
"""
from time import sleep

from regie_pkg.mysql_connect import MySQLConnect

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
