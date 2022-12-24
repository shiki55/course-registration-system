"""
This module contains configuration information for testing.

Global fixtures and plugins that can be used across tests are defined here.
Fixtures defined here can be used in tests without needing to explicitly import them.
"""

import pytest
import json
import os, sys, inspect
##
curr_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
##

from regie_pkg.mysql_connect import MySQLConnect
from regie_pkg.get_mongo_client import get_mongo_client
from regie_pkg.mongodb import MongoDB

@pytest.fixture(scope="function", autouse=True) # run automatically for every test function
def test_mysql():
    """
    "Ensure that the test MySQL database is set up and torn down for each test."

    This fixture creates a new MySQL database for testing named "REGIE_db_test",
    creates tables in the database using the SQL statements in 'database_files/create_table.sql',
    and populates the tables with test data using the SQL statements in
    'test_data/mysql_test_data.sql'. The fixture also resets the MySQLConnect singleton
    to use the production database "REGIE_db" after the test is finished.
    """
    MySQLConnect.set_database(None)

    # Create the test database
    mysql_conn = MySQLConnect()
    test_db_name = "REGIE_db_test"
    mysql_conn.execute_query(f'CREATE DATABASE {test_db_name};')
    MySQLConnect.set_database(test_db_name)

    # create tables
    with open('../../database_files/create_table.sql', encoding='utf-8') as f:
        mysql_conn.execute_query(f.read(), multi=True)

    # populate tables with test data
    with open('./test_data/mysql_test_data.sql', encoding='utf-8') as f:
        mysql_conn.execute_query(f.read(), multi=True, commit=True)

    yield

    # drop db after test and point MySQLConnect to prod database
    mysql_conn.execute_query(f'DROP DATABASE IF EXISTS {test_db_name};')
    prod_db_name = "REGIE_db"
    MySQLConnect.set_database(prod_db_name)

@pytest.fixture(scope="function", autouse=True) # run automatically for every test function
def test_mongodb():
    """
    "Ensure that the test MongoDB database is set up and torn down for each test."

    This fixture creates a new MongoDB database for testing named ""credential_db_test"",
    creates a collection "student", and populates the collection with test data from
    test_data/mongodb_test_data.json.
    The fixture also resets MongoDB class to reference the production db "credential_db" after
    each test.
    """
    mongo_client = get_mongo_client()
    test_db_name = "credential_db_test"
    credential_db = mongo_client[test_db_name]
    student = credential_db['student'] # student collection
    with open('./test_data/mongodb_test_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        student.insert_many(data)

    MongoDB.set_database(test_db_name)

    yield

    mongo_client.drop_database(test_db_name)
    prod_db_name = "credential_db"
    MongoDB.set_database(prod_db_name)
