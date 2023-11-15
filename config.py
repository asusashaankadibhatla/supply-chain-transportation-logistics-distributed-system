params = {
    "host": "localhost",  # Replace with your CockroachDB host address
    "port": "26257",  # Default port for CockroachDB
    "dbname": "defaultdb",  # Replace with your database name
    "user": "your_username",
    "password": "your_password",
    "sslmode": "require",  # or "verify-full" if you have SSL certificates
    # If using SSL certificates, you may also need the following:
    # "sslrootcert": "path/to/root.crt",
    # "sslcert": "path/to/client.<username>.crt",
    # "sslkey": "path/to/client.<username>.key"
}
