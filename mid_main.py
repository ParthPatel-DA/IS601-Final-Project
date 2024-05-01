# Parth Patel
# Mid Term Project
# IS601 - 1J2

import json
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


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser()
#     parser.add_argument('filename')

#     args = parser.parse_args()
#     filename = args.filename

#     read_and_make_json_file(filename)