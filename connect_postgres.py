import psycopg2
from config import params
DEFAULT_DBNAME = 'defaultdb'

def connect_cockroachdb(dbname=DEFAULT_DBNAME):
    try:
        # CockroachDB connection details
        user = params['user']
        password = params['password']
        host = params['host']
        port = params['port']
        sslmode = params.get('sslmode', 'require')  # Default SSL mode

        # Construct the connection string
        conn_string_parts = [
            f"dbname='{dbname}'",
            f"user='{user}'",
            f"host='{host}'",
            f"password='{password}'",
            f"port='{port}'",
            f"sslmode='{sslmode}'"
        ]

        # Additional SSL parameters, if provided
        if 'sslrootcert' in params:
            conn_string_parts.append(f"sslrootcert='{params['sslrootcert']}'")
        if 'sslcert' in params:
            conn_string_parts.append(f"sslcert='{params['sslcert']}'")
        if 'sslkey' in params:
            conn_string_parts.append(f"sslkey='{params['sslkey']}'")

        # Finalize the connection string
        conn_string = " ".join(conn_string_parts)

        # Connect to the CockroachDB cluster
        conn = psycopg2.connect(conn_string)

        # Print a success message
        print("Successfully connected to CockroachDB with database:", dbname)

        # Return the connection
        return conn
    except Exception as e:
        print("Error: Unable to connect to CockroachDB")
        print(e)
        return None
