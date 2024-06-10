import sqlite3

DATABASE_NAME = './database/magazine.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

connection = get_db_connection()
if connection:
    create_tables(connection)
    connection.close()
else:
    print("Could not connect to the database")
