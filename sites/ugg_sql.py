import sqlite3
import os

# DB_FILE = 'ugg.db'

dir_path = os.path.dirname(os.path.realpath(__file__))

# Construct the absolute path to the database
DB_FILE = os.path.join(dir_path, 'ugg.db')


class ugg_order:
    def __init__(self, orderNumber, price, tracking, status, link, date, products, id):
        self.orderNumber = orderNumber
        self.price = price
        self.tracking = tracking
        self.status = status
        self.link = link
        self.date = date
        self.products = products
        self.id = id
    # def prod_add(self):


def table_exists(table_name):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name=?;", (table_name,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def create_table():
    if not table_exists('order_info'):
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_info (
                id INTEGER PRIMARY KEY,
                order_number INTEGER NOT NULL,
                price TEXT,
                tracking_number TEXT,
                delivery_status TEXT,
                link TEXT,       
                date TEXT,      
                products TEXT  
            )
        ''')
        conn.commit()
        conn.close()


def add_order(order_number):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM order_info WHERE order_number = ?', (order_number,))
    existing_order = cursor.fetchone()

    if existing_order:
        print(f"Order number {order_number} already exists.")
    else:
        cursor.execute('''
            INSERT INTO order_info (order_number)
            VALUES (?)
        ''', (order_number,))

        print(f"Order number {order_number} added successfully.")

    conn.commit()
    conn.close()


def update_order_info(order_number, price=None, tracking_number=None, delivery_status=None, link=None, date=None,
                      products=None):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    update_parts = []
    params = []

    if price is not None:
        update_parts.append("price = ?")
        params.append(price)

    if tracking_number is not None:
        update_parts.append("tracking_number = ?")
        params.append(tracking_number)

    if delivery_status is not None:
        update_parts.append("delivery_status = ?")
        params.append(delivery_status)

    if link is not None:
        update_parts.append("link = ?")
        params.append(link)

    if date is not None:
        update_parts.append("date = ?")
        params.append(date)

    if products is not None:
        update_parts.append("products = ?")
        params.append(products)

    # Add more fields here as necessary

    params.append(order_number)  # Adding the order_number to the parameters list for the WHERE clause

    if update_parts:
        update_query = "UPDATE order_info SET " + ", ".join(update_parts) + " WHERE order_number = ?"
        cursor.execute(update_query, params)
        print("Updated order {} info".format(order_number))

    conn.commit()
    conn.close()


def get_order_info(order_number):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM order_info WHERE order_number = ?', (order_number,))
    row = cursor.fetchone()

    conn.close()
    if row:
        return ugg_order(orderNumber=row[1], price=row[2], tracking=row[3], status=row[4], link=row[5], date=row[6],
                            products=row[7], id=None)
    return None


def get_all_order_numbers():
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('SELECT order_number FROM order_info ORDER BY order_number DESC')
    rows = cursor.fetchall()

    conn.close()
    return [row[0] for row in rows]


def get_all_order_info():

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM order_info ORDER BY order_number DESC')
    rows = cursor.fetchall()

    conn.close()

    allOrders = []
    count = 0
    for row in rows:
        count += 1
        uggProd = ugg_order(orderNumber=row[1], price=row[2], tracking=row[3], status=row[4], link=row[5], date=row[6],
                            products=row[7], id=count)
        allOrders.append(uggProd)

    return allOrders


def delete_order(order_number):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute('DELETE FROM order_info WHERE order_number = ?', (order_number,))
    conn.commit()
    conn.close()
