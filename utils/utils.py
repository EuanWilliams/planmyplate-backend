"""A collection of functions and classes used throughout the codebase"""

import os
import dotenv
import mysql
import mysql.connector


def get_database_connection() -> mysql.connector.connection.MySQLConnection:
    """Returns a connection to the database"""

    dotenv.load_dotenv()

    DB_HOST = os.getenv("PMP_DATABASE_HOST")
    DB_PASS = os.getenv("PMP_DATABASE_PASS")
    DB_USER = os.getenv("PMP_DATABASE_USER")
    DB_NAME = os.getenv("PMP_DATABASE_NAME")
    DB_PORT = os.getenv("PMP_DATABASE_PORT")

    try:
        return mysql.connector.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASS, db=DB_NAME, port=DB_PORT)
    except Exception as error:
        print(f"ERROR: Could not connect to database: {error}")
    return None
