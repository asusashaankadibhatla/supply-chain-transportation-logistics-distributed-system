import psycopg2
from config import params
DEFAULT_DBNAME = 'postgres'

def connect_postgres(dbname = DEFAULT_DBNAME):
    try:
        # PostgreSQL connection details
        user = params['user']
        password = params['password']
        host = params['host']
        port = params['port']

        # Construct the connection string
        conn_string = f"dbname='{dbname}' user='{user}' host='{host}' password='{password}' port='{port}'"

        # Connect to the PostgreSQL database
        conn = psycopg2.connect(conn_string)

        # Print a success message
        print("Successfully connected to PostgreSQL! with ",dbname)

        # Return the connection
        return conn
    except Exception as e:
        print("Error: Unable to connect to PostgreSQL")
        print(e)
        return None
