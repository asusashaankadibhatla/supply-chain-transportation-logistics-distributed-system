import psycopg2
import datetime
from config import params

class BaseDistributedTable:
    def __init__(self, connection):
        self.connection = connection

    def _execute_query(self, query):
        with self.connection.cursor() as cursor:
            cursor.execute(query)
            self.connection.commit()

class CustomersDistributedTable(BaseDistributedTable):

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Customers (
            CustomerID SERIAL PRIMARY KEY,
            CustomerName VARCHAR(255) NOT NULL,
            ContactInfo VARCHAR(255),
            CustomerStatus VARCHAR(50),
            JoinDate DATE NOT NULL,
            LastPurchaseDate DATE,
            INDEX join_date_idx (JoinDate)
        ) PARTITION BY RANGE (JoinDate);
        """
        self._execute_query(create_table_query)

    def check_and_create_partition(self, join_date):
        # Calculate the partition range based on the join_date
        start_of_year = datetime.date(join_date.year, 1, 1)
        end_of_year = datetime.date(join_date.year + 1, 1, 1)

        partition_name = f"customers_{join_date.year}"

        # Create the partition if it does not exist
        partition_query = f"""
        ALTER TABLE Customers PARTITION BY RANGE (JoinDate) ADD IF NOT EXISTS PARTITION {partition_name} VALUES FROM ('{start_of_year}') TO ('{end_of_year}');
        """
        self._execute_query(partition_query)

    def insert_customer(self, customer_data):
        # Assume customer_data is a dictionary with necessary customer info
        join_date = customer_data["JoinDate"]

        # Check if a new partition is needed
        self.check_and_create_partition(join_date)

        # Insert the new customer
        insert_query = f"""
        INSERT INTO Customers (CustomerName, ContactInfo, CustomerStatus, JoinDate, LastPurchaseDate)
        VALUES (%s, %s, %s, %s, %s);
        """
        with self.connection.cursor() as cursor:
            cursor.execute(insert_query, (customer_data["CustomerName"], customer_data["ContactInfo"], customer_data["CustomerStatus"], customer_data["JoinDate"], customer_data["LastPurchaseDate"]))
            self.connection.commit()

# Usage example
connection = psycopg2.connect(**params)
customers_db = CustomersDistributedTable(connection)

# Insert a new customer
new_customer = {
    "CustomerName": "John Doe",
    "ContactInfo": "johndoe@example.com",
    "CustomerStatus": "Active",
    "JoinDate": datetime.date.today(),
    "LastPurchaseDate": datetime.date.today()
}
customers_db.insert_customer(new_customer)

connection.close()
