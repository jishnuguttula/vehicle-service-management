import sqlite3

conn = sqlite3.connect('service_center.db')

cursor = conn.cursor()

# customers table
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    name TEXT,

    phone TEXT,

    vehicle_number TEXT
)
''')

# services table
cursor.execute('''
CREATE TABLE IF NOT EXISTS services (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    customer_name TEXT,

    service_type TEXT
)
''')

conn.commit()

conn.close()

print("Database Created Successfully")