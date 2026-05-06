from flask import Flask, redirect, render_template, request, session
import sqlite3

app = Flask(__name__)
app.secret_key = 'secret123'

# home page
@app.route('/')
def home():
    return render_template('index.html')

# login page
@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        username = request.form['username']
        password = request.form['password']

        if username == "admin" and password == "admin123":

            session['admin'] = username

            return redirect('/dashboard')

        else:

            return "Invalid Credentials"

    return render_template('login.html')



# dashboard page
@app.route('/dashboard')
def dashboard():

    if 'admin' not in session:
        return redirect('/login')

    conn = sqlite3.connect('service_center.db')

    cursor = conn.cursor()

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            vehicle_number TEXT
        )
        '''
    )

    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS services (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            service_type TEXT,
            amount INTEGER
        )
        '''
    )

    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM customers")
    customers = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM services")
    services = cursor.fetchone()[0]

    revenue = 0

    conn.close()

    return render_template(
        'dashboard.html',
        customers=customers,
        services=services,
        revenue=revenue
    )


# add customers
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():

    if request.method == 'POST':

        name = request.form['name']
        phone = request.form['phone']
        vehicle_number = request.form['vehicle_number']

        conn = sqlite3.connect('service_center.db')

        cursor = conn.cursor()

        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS customers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                phone TEXT,
                vehicle_number TEXT
            )
            '''
        )

        cursor.execute(
            '''
            INSERT INTO customers(name, phone, vehicle_number)
            VALUES (?, ?, ?)
            ''',
            (name, phone, vehicle_number)
        )

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('add_customer.html')

# view customers
@app.route('/customers')
def customers():
    conn = sqlite3.connect('service_center.db')
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM customers")
    data = cursor.fetchall()

    conn.close()

    return render_template('customers.html', data=data)

# add service
@app.route('/add_service', methods=['GET', 'POST'])
def add_service():

    if request.method == 'POST':

        customer_name = request.form['customer_name']
        service_type = request.form['service_type']

        conn = sqlite3.connect('service_center.db')

        cursor = conn.cursor()

        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS services (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT,
                service_type TEXT
            )
            '''
        )

        cursor.execute(
            '''
            INSERT INTO services(customer_name, service_type)
            VALUES (?, ?)
            ''',
            (customer_name, service_type)
        )

        conn.commit()
        conn.close()

        return redirect('/dashboard')

    return render_template('add_service.html')
# view services
@app.route('/services')
def services():
    conn = sqlite3.connect('service_center.db')
    cursor = conn.cursor()

    cursor.execute('''
    SELECT services.id, customers.name, services.service_type, services.Mechanic_name, services.service_date, services.status, services.Bill
    FROM services
    JOIN customers ON services.customer_id = customers.id
    ''')
    data = cursor.fetchall()

    conn.close()

    return render_template('services.html', data=data)

# logout
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect('/login')

if __name__ == '__main__':
    app.run(debug=True)