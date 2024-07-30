import sqlite3
import os
from flask import Flask

# SQLite database file path
db_file = 'DonJohn.db'

app = Flask(__name__)

# Function to initialize the database
def initialize_database():
    if os.path.exists(db_file):
        # Connect to the SQLite database
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()

        # Check if tables already exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name IN ('Provinces', 'City', 'FullfilementTypes')")
        existing_tables = cursor.fetchall()

        # Check if triggers already exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='trigger'")
        existing_triggers = cursor.fetchall()

        # Check if tables already contain data
        cursor.execute("SELECT COUNT(*) FROM Provinces")
        existing_data = cursor.fetchone()[0] > 0

        # Close the connection
        conn.close()

        # If tables, triggers, or data already exist, don't execute the scripts
        if existing_tables or existing_triggers or existing_data:
            print("Tables, triggers, or data already exist. Skipping script execution.")
            return
    else:
        print("Database file does not exist. Creating new database.")
        conn = sqlite3.connect(db_file)
        conn.close()

    # Execute create_tables.sql
    with open('create_tables.sql', 'r') as f:
        create_tables_sql = f.read()
    conn = sqlite3.connect(db_file)
    conn.executescript(create_tables_sql)
    conn.close()

    # Execute create_triggers.sql
    with open('create_triggers.sql', 'r') as f:
        create_triggers_sql = f.read()
    conn = sqlite3.connect(db_file)
    conn.executescript(create_triggers_sql)
    conn.close()

    # Execute insert_constants.sql
    with open('insert_constants.sql', 'r') as f:
        insert_constants_sql = f.read()
    conn = sqlite3.connect(db_file)
    conn.executescript(insert_constants_sql)
    conn.close()

# Call the function to initialize the database
initialize_database()


