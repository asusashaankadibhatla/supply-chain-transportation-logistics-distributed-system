import psycopg2
from config import params
from connect_postgres import connect_postgres

def create_database(dbname):
    try:
        # Connect to CockroachDB
        conn = connect_postgres('system')  # Connect to the 'system' database to create a new database

        # Create a cursor object
        cursor = conn.cursor()

        # Execute SQL command to create the specified database
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbname};")

        # Commit the changes
        conn.commit()

        # Print a success message
        print(f"Database '{dbname}' created successfully.")

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except Exception as e:
        print(f"Error: Unable to create database '{dbname}'.")
        print(e)

if __name__ == "__main__":
    create_database(params["dbname"])
