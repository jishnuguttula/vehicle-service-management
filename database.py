import sqlite3

conn = sqlite3.connect('service_center.db')

cursor = conn.cursor()

#customer table
cursor.execute('''
CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    phone TEXT,
    address TEXT,
    vechile_model TEXT,
    vechile_number TEXT UNIQUE
)
''')

# service table
cursor.execute('''
CREATE TABLE IF NOT EXISTS services (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER,
    service_type TEXT NOT NULL,
    Mechanic_name TEXT NOT NULL,
    service_date TEXT NOT NULL,
    status TEXT NOT NULL,
    Bill REAL,
    FOREIGN KEY (customer_id) REFERENCES customers (id)
)
''')

# admin Table
cursor.execute('''
CREATE TABLE IF NOT EXISTS admins ( 
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
)
''')

# default admin
cursor.execute("INSERT INTO admins (username, password) VALUES ('admin', 'admin123')")
               
conn.commit()
conn.close()

print("Database and tables created successfully!") 