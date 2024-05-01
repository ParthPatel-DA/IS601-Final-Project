# Parth Patel
# Mid Term Project
# IS601 - 1J2

import json
import sqlite3
import os
# import argparse

def read_json_file(filename):
    """
    Utility Function - Reads a JSON file and returns the data as a dictionary
    """
    with open(filename, 'r') as file:
        data = json.load(file)
    return data

def write_json_file(filename, data):
    """Utility Function - Writes a dictionary to a JSON file"""
    with open(filename, 'w') as file:
        json.dump(data, file)

def sort_data(data):
    """Utility Function - Sorts a dictionary by key"""
    return dict(sorted(data, key=lambda x: x[0]))

def generate_customer_data(data):
    """Generates a dictionary of customer data"""
    customer_data = {}
    for order in data:
        customer_data[order['phone']] = order['name']
    return customer_data

def generate_order_data(data):
    """Generates a dictionary of order data"""
    order_data = {}
    for order in data:
        for item in order['items']:
            if item['name'] in order_data:
                order_data[f"{item['name']}"]['orders'] += 1
            else:
                order_data[f"{item['name']}"] = {
                    'price': item['price'],
                    'orders': 1
                }
    return order_data

def read_and_make_json_file(filename):
    """Reads a JSON file and generates two new JSON files"""
    data = read_json_file(filename)
    write_json_file('customers.json', generate_customer_data(data))
    write_json_file('items.json', generate_order_data(data))

def create_tables():
    """Creates the database tables"""
    os.remove("data.db") if os.path.exists("data.db") else None

    con = sqlite3.connect("data.db")
    cur = con.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS customers(
            id INTEGER PRIMARY KEY,
            name CHAR(64) NOT NULL,
            phone CHAR(10) NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS items(
            id INTEGER PRIMARY KEY,
            name CHAR(64) NOT NULL,
            price REAL NOT NULL
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            cust_id INT NOT NULL,
            notes TEXT,
            FOREIGN KEY(cust_id) REFERENCES customers(id)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS item_list(
            order_id NOT NULL,
            item_id NOT NULL,
            FOREIGN KEY(order_id) REFERENCES orders(id),
            FOREIGN KEY(item_id) REFERENCES items(id)
        );
    """)

    con.commit()
    con.close()

def load_data_into_tables():
    """Loads data into the database tables"""
    con = sqlite3.connect("data.db")
    cur = con.cursor()

    data = read_json_file("example_orders.json")

    for phone, name in generate_customer_data(data).items():
        cur.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (name, phone))

    for name, item in generate_order_data(data).items():
        cur.execute("INSERT INTO items (name, price) VALUES (?, ?);", (name, item['price']))

    for order in data:
        # read the customer id
        cur.execute("SELECT id FROM customers WHERE phone = ?;", (order['phone'],))
        cust_id = cur.fetchone()[0]

        if cust_id is None:
            print("Customer ID not found")
            continue

        # insert the order
        cur.execute("INSERT INTO orders (timestamp, cust_id, notes) VALUES (?, ?, ?);", (order['timestamp'], cust_id, order['notes']))

        # cur.execute("SELECT last_insert_rowid();")
        order_id = cur.lastrowid
        
        for item in order['items']:
            cur.execute("SELECT id FROM items WHERE name = ?;", (item['name'],))
            item_id = cur.fetchone()[0]

            if item_id is None:
                print("Item ID not found")
                continue

            cur.execute("INSERT INTO item_list (order_id, item_id) VALUES (?, ?);", (order_id, item_id))

    con.commit()
    con.close()

# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('filename')

#     args = parser.parse_args()
#     filename = args.filename

#     read_and_make_json_file(filename)