import psycopg2
import random
import datetime
from config import params

# Assuming your CustomersDistributedTable class is defined as before

def generate_random_date(year):
    # Generate a random date within a given year
    start_date = datetime.date(year, 1, 1)
    end_date = datetime.date(year, 12, 31)
    delta = end_date - start_date
    random_days = random.randrange(delta.days)
    return start_date + datetime.timedelta(days=random_days)

def generate_customers(num_customers):
    customers = []
    for i in range(1, num_customers + 1):
        customer_name = f"Customer{i:05d}"  # Generates names like Customer00001, Customer00002, etc.
        contact_info = f"customer{i:05d}@example.com"
        customer_status = random.choice(["Active", "Inactive"])
        join_date = generate_random_date(2023)  # You can set the year as needed
        last_purchase_date = join_date + datetime.timedelta(days=random.randint(0, 30))  # Last purchase within 30 days of joining

        customer = {
            "CustomerName": customer_name,
            "ContactInfo": contact_info,
            "CustomerStatus": customer_status,
            "JoinDate": join_date,
            "LastPurchaseDate": last_purchase_date
        }
        customers.append(customer)
    return customers

def bulk_insert_customers(connection, customers):
    insert_query = """
    INSERT INTO Customers (CustomerName, ContactInfo, CustomerStatus, JoinDate, LastPurchaseDate)
    VALUES (%s, %s, %s, %s, %s);
    """
    with connection.cursor() as cursor:
        for customer in customers:
            cursor.execute(insert_query, (customer["CustomerName"], customer["ContactInfo"], customer["CustomerStatus"], customer["JoinDate"], customer["LastPurchaseDate"]))
    connection.commit()

# Establish the database connection
connection = psycopg2.connect(**params)

# Generate 10000 customers
customers = generate_customers(10000)

# Bulk insert customers
bulk_insert_customers(connection, customers)

# Close the connection
connection.close()
