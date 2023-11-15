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

class SuppliersDistributedTable(BaseDistributedTable):

    def create_table(self):
        create_table_query = """
        CREATE TABLE IF NOT EXISTS Suppliers (
            SupplierID SERIAL PRIMARY KEY,
            SupplierName VARCHAR(255) NOT NULL,
            ContactInfo VARCHAR(255),
            SupplierStatus VARCHAR(50),
            PerformanceRating INT,
            LastReviewDate DATE,
            ContractStartDate DATE NOT NULL,
            ContractEndDate DATE,
            INDEX contract_start_date_idx (ContractStartDate)
        ) PARTITION BY RANGE (ContractStartDate);
        """
        self._execute_query(create_table_query)

    def check_and_create_partition(self, contract_start_date):
        # Calculate the partition range based on the contract_start_date
        start_of_year = datetime.date(contract_start_date.year, 1, 1)
        end_of_year = datetime.date(contract_start_date.year + 1, 1, 1)

        partition_name = f"suppliers_{contract_start_date.year}"

        # Create the partition if it does not exist
        partition_query = f"""
        ALTER TABLE Suppliers PARTITION BY RANGE (ContractStartDate) ADD IF NOT EXISTS PARTITION {partition_name} VALUES FROM ('{start_of_year}') TO ('{end_of_year}');
        """
        self._execute_query(partition_query)

    def insert_supplier(self, supplier_data):
        # Assume supplier_data is a dictionary with necessary supplier info
        contract_start_date = supplier_data["ContractStartDate"]

        # Check if a new partition is needed
        self.check_and_create_partition(contract_start_date)

        # Insert the new supplier
        insert_query = f"""
        INSERT INTO Suppliers (SupplierName, ContactInfo, SupplierStatus, PerformanceRating, LastReviewDate, ContractStartDate, ContractEndDate)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
        """
        with self.connection.cursor() as cursor:
            cursor.execute(insert_query, (supplier_data["SupplierName"], supplier_data["ContactInfo"], supplier_data["SupplierStatus"], supplier_data["PerformanceRating"], supplier_data["LastReviewDate"], supplier_data["ContractStartDate"], supplier_data["ContractEndDate"]))
            self.connection.commit()

# Usage example
connection = psycopg2.connect(**params)
suppliers_db = SuppliersDistributedTable(connection)

# Insert a new supplier
new_supplier = {
    "SupplierName": "Acme Corp",
    "ContactInfo": "contact@acmecorp.com",
    "SupplierStatus": "Active",
    "PerformanceRating": 5,
    "LastReviewDate": datetime.date.today(),
    "ContractStartDate": datetime.date.today(),
    "ContractEndDate": datetime.date.today() + datetime.timedelta(days=365)
}
suppliers_db.insert_supplier(new_supplier)

connection.close()
