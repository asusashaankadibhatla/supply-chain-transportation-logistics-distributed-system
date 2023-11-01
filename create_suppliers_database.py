import psycopg2
from config import params
from connect_postgres import connect_postgres
from create_database import create_database

class SuppliersDistributedDatabase:

    def __init__(self, params, replication_factor):
        self.connection = psycopg2.connect(**params)
        self.replication_factor = replication_factor

    def create_table_query(self):
        return """
        CREATE TABLE IF NOT EXISTS Suppliers (
            SupplierID SERIAL PRIMARY KEY,
            SupplierName VARCHAR(255) NOT NULL,
            ContactInfo VARCHAR(255),
            SupplierStatus VARCHAR(50),
            PerformanceRating INT,
            LastReviewDate DATE,
            ContractStartDate DATE NOT NULL,
            ContractEndDate DATE
        ) PARTITION BY RANGE(EXTRACT(YEAR FROM ContractStartDate), EXTRACT(MONTH FROM ContractStartDate));
        """

    def trigger_function_query(self):
        return """
        DO $$
        BEGIN
            IF NOT EXISTS(SELECT relname FROM pg_class WHERE relname='suppliers_' || to_char(NEW.ContractStartDate, 'YYYY_MM')) THEN
                EXECUTE 'CREATE TABLE suppliers_' || to_char(NEW.ContractStartDate, 'YYYY_MM') || ' PARTITION OF Suppliers FOR VALUES FROM (' || EXTRACT(YEAR FROM NEW.ContractStartDate) || ', ' || EXTRACT(MONTH FROM NEW.ContractStartDate) || ') TO (' || EXTRACT(YEAR FROM NEW.ContractStartDate) + (CASE WHEN EXTRACT(MONTH FROM NEW.ContractStartDate) = 12 THEN 1 ELSE 0 END) || ', ' || (CASE WHEN EXTRACT(MONTH FROM NEW.ContractStartDate) = 12 THEN 1 ELSE EXTRACT(MONTH FROM NEW.ContractStartDate) + 1 END) || ');';
            END IF;
        END;
        $$ LANGUAGE plpgsql;
        """

    def create_trigger_query(self):
        return """
        CREATE TRIGGER insert_suppliers_trigger
        BEFORE INSERT ON Suppliers
        FOR EACH ROW EXECUTE FUNCTION create_suppliers_partition();
        """

    def distribute_table_query(self):
        return f"""
        SELECT create_distributed_table('Suppliers', 'ContractStartDate');
        """

    def set_replication_factor_query(self):
        return f"""
        SELECT set_replication_factor('Suppliers', {self.replication_factor});
        """
    
    def initialize_citus_query(self):
        return """
        CREATE EXTENSION IF NOT EXISTS citus;
        """
    
    def _execute_query(self, query):
        cursor = self.connection.cursor()
        cursor.execute(query)
        cursor.close()

    def setup_database(self):
        # Initialize the Citus extension
        self._execute_query(self.initialize_citus_query())

        # Create the Suppliers table with partitioning definition
        self._execute_query(self.create_table_query())

        # Trigger function to dynamically create partitions if they don't exist
        self._execute_query(self.trigger_function_query())

        # Attach the trigger to the Suppliers table
        self._execute_query(self.create_trigger_query())

        # Using Citus to distribute the parent table based on the partition key
        self._execute_query(self.distribute_table_query())

        # Set replication factor
        self._execute_query(self.set_replication_factor_query())

        # Commit the transaction
        self.connection.commit()

    def close(self):
        self.connection.close()

if __name__ == "__main__":
    db = SuppliersDistributedDatabase(params, replication_factor=2)
    db.setup_database()
    db.close()
