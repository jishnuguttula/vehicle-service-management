import sqlite3

conn = sqlite3.connect('service_center.db')

cursor = conn.cursor()

# delete old tables if they exist
cursor.execute("DROP TABLE IF EXISTS customers")
cursor.execute("DROP TABLE IF EXISTS services")

# customers table
cursor.execute('''
CREATE TABLE customers (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    phone TEXT,

    vehicle_number TEXT
)
''')

# services table
cursor.execute('''
CREATE TABLE services (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_name TEXT,

    service_type TEXT
)
''')

conn.commit()

conn.close()

print("Fresh Database Created Successfully")