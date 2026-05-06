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

        conn = sqlite3.connect('service_center.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM admins WHERE username=? AND password=?", (username, password))
        admin = cursor.fetchone()

        conn.close()

        if admin:
            session['admin'] = username
            return redirect('/dashboard')
        else:
            return render_template('login.html', error='Invalid credentials. Please try again.')

    return render_template('login.html')



# dashboard page
@app.route('/dashboard')
def dashboard():
    if 'admin' not in session:
        return redirect('/login')
    conn = sqlite3.connect('service_center.db')
    cursor = conn.cursor()  

    cursor.execute("SELECT * FROM customers")
    total_customers = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM services")
    total_services = cursor.fetchone()[0]

    cursor.execute("SELECT SUM(Bill) FROM services")
    revenue = cursor.fetchone()[0]

    conn.close()

    return render_template('dashboard.html',
                            total_customers=total_customers, 
                            total_services=total_services,
                            revenue=revenue)


# add customers
@app.route('/add_customer', methods=['GET', 'POST'])
def add_customer():

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        vechile_model = request.form['vechile_model']
        vechile_number = request.form['vechile_number']

        conn = sqlite3.connect('service_center.db')
        cursor = conn.cursor()

        cursor.execute("INSERT INTO customers (name, email, phone, address, vechile_model, vechile_number) VALUES (?, ?, ?, ?, ?, ?)",
                       (name, email, phone, address, vechile_model, vechile_number))
        
        conn.commit()
        conn.close()

        return redirect('/customers')
        
    return render_template('customer.html')

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

    conn = sqlite3.connect('service_center.db')
    cursor = conn.cursor()  

    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()

    if request.method == 'POST':
        customer_id = request.form['customer_id']
        service_type = request.form['service_type']
        Mechanic_name = request.form['Mechanic_name']
        service_date = request.form['service_date']
        status = request.form['status']
        Bill = request.form['Bill']

        cursor.execute("INSERT INTO services (customer_id, service_type, Mechanic_name, service_date, status, Bill) VALUES (?, ?, ?, ?, ?, ?)",
                       (customer_id, service_type, Mechanic_name, service_date, status, Bill))
        
        conn.commit()
        conn.close()

        return redirect('/services')
    conn.close()
    return render_template('service.html', customers=customers)

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