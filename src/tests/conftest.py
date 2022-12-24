"""
This module contains configuration information for testing.

Global fixtures and plugins that can be used across tests are defined here.
Fixtures defined here can be used in tests without needing to explicitly import them.
"""

import pytest
import os, sys, inspect
##
curr_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parent_dir = os.path.dirname(curr_dir)
sys.path.append(parent_dir)
##

from regie_pkg.mysql_connect import MySQLConnect

@pytest.fixture(scope="function", autouse=True) # run automatically for every test function
def test_db():
    """
    "Ensure that the test database is set up and torn down for each test."

    This fixture creates a new MySQL database for testing named "REGIE_db_test",
    creates tables in the database using the SQL statements in 'sql_files/create_table.sql',
    and populates the tables with test data using the SQL statements in 'tests/populate_test.sql'.
    The fixture also resets the MySQLConnect singleton to use the production database
    "REGIE_db" after the test is finished.
    """
    MySQLConnect.set_database(None)

    # Create the test database
    mysql_conn = MySQLConnect()
    test_db_name = "REGIE_db_test"
    mysql_conn.execute_query(f'CREATE DATABASE {test_db_name};')
    MySQLConnect.set_database(test_db_name)

    # create tables
    with open('../../sql_files/create_table.sql', encoding='utf-8') as f:
        mysql_conn.execute_query(f.read(), multi=True)

    # populate tables with test data
    with open('populate_test.sql', encoding='utf-8') as f:
        mysql_conn.execute_query(f.read(), multi=True, commit=True)

    yield

    # drop db after test and point MySQLConnect to prod database
    mysql_conn.execute_query(f'DROP DATABASE IF EXISTS {test_db_name};')
    prod_db_name = "REGIE_db"
    MySQLConnect.set_database(prod_db_name)