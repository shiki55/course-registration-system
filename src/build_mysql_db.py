"""
Build a MySQL database for the REGIE application.

This module is responsible for setting up and populating a
MySQL database for the REGIE project. It first drops the REGIE_db
database if it exists, then creates a new REGIE_db database.
It then creates the tables in the REGIE_db database using the
create_table.sql file and populates the tables using the populate.sql file.

Note:
- The MySQL server must be running and accessible.
"""

from time import sleep

from regie_pkg.mysql_connect import MySQLConnect

MySQLConnect.set_database(None)
mysql_conn = MySQLConnect()
mysql_conn.execute_query('DROP DATABASE IF EXISTS REGIE_db;')
mysql_conn.execute_query('CREATE DATABASE REGIE_db;')
MySQLConnect.set_database("REGIE_db")

sleep(1)

# create tables
with open('../sql_files/create_table.sql', encoding='utf-8') as f:
    mysql_conn.execute_query(f.read(), multi=True)

sleep(2)

# populate tables
with open('../sql_files/populate.sql', encoding='utf-8') as f:
    mysql_conn.execute_query(f.read(), multi=True, commit=True)
