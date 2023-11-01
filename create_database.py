import psycopg2
from config import params
from connect_postgres import connect_postgres
def create_database(dbname):

    try:
        # Connect to PostgreSQL
        conn = connect_postgres()

        # Disable autocommit to allow database creation
        conn.autocommit = True

        # Create a cursor object
        cursor = conn.cursor()

        # Execute SQL command to create the specified database
        cursor.execute(f"CREATE DATABASE {dbname};")

        # Revert autocommit setting
        conn.autocommit = False

        # Print a success message
        print(f"Database '{dbname}' created successfully.")

        # Close the cursor and connection
        cursor.close()
    except Exception as e:
        print(f"Error: Unable to create database '{dbname}'")
        print(e)
if __name__ == "__main__":
    create_database(params['dbname'])