import psycopg2
import random
import datetime
from config import params

# Assuming your SuppliersDistributedTable class is defined as before

def generate_random_date(year):
    # Generate a random date within a given year
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    return start_date + datetime.timedelta(days=random_days)

def generate_suppliers(num_suppliers):
    suppliers = []
    for i in range(1, num_suppliers + 1):
        supplier_name = f"Supplier{i:05d}"  # Generates names like Supplier00001, Supplier00002, etc.
        contact_info = f"supplier{i:05d}@example.com"
        supplier_status = random.choice(["Active", "Inactive"])
        performance_rating = random.randint(1, 5)  # Random performance rating between 1 and 5
        contract_start_date = generate_random_date(2023)  # You can set the year as needed
        contract_end_date = contract_start_date + datetime.timedelta(days=365)  # Contract duration of one year

        supplier = {
            "SupplierName": supplier_name,
            "ContactInfo": contact_info,
            "SupplierStatus": supplier_status,
            "PerformanceRating": performance_rating,
            "LastReviewDate": contract_start_date - datetime.timedelta(days=random.randint(10, 60)),  # Random review date before the contract starts
            "ContractStartDate": contract_start_date,
            "ContractEndDate": contract_end_date
        }
        suppliers.append(supplier)
    return suppliers

def bulk_insert_suppliers(connection, suppliers):
    insert_query = """
    INSERT INTO Suppliers (SupplierName, ContactInfo, SupplierStatus, PerformanceRating, LastReviewDate, ContractStartDate, ContractEndDate)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    with connection.cursor() as cursor:
        for supplier in suppliers:
            cursor.execute(insert_query, (supplier["SupplierName"], supplier["ContactInfo"], supplier["SupplierStatus"], supplier["PerformanceRating"], supplier["LastReviewDate"], supplier["ContractStartDate"], supplier["ContractEndDate"]))
    connection.commit()

# Establish the database connection
connection = psycopg2.connect(**params)

# Generate 10,000 suppliers
suppliers = generate_suppliers(10000)

# Bulk insert suppliers
bulk_insert_suppliers(connection, suppliers)

# Close the connection
connection.close()
