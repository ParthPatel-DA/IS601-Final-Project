from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
import sqlite3
from schemas import Customer, Item, Order, OrderDetails

class Response:
    def __init__(self, message, data, code):
        self.message = message
        self.data = data
        self.code = code

class ErrorResponse:
    def __init__(self, message, code):
        self.message = message
        self.code = code

app = FastAPI()

# con = sqlite3.connect("data.db")
# cur = con.cursor()

def get_db_cursor():
    con = sqlite3.connect("data.db", check_same_thread=False)
    try:
        cursor = con.cursor()
        yield cursor
    finally:
        con.commit()
        con.close()

@app.get("/", tags=["Root"])
async def root():
    return Response("Success!", None, 200)

@app.get("/customers/{id}", tags=["Customers"])
async def get_customer(id: int, cur: sqlite3.Cursor = Depends(get_db_cursor)):
    cur.execute("SELECT * FROM customers WHERE id = ?;", (id,))
    data = cur.fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return Response("Customer found", Customer(id=data[0], name=data[1], phone=data[2]), 200)

@app.post("/customers", tags=["Customers"])
async def create_customer(customer: Customer, cur: sqlite3.Cursor = Depends(get_db_cursor)):
    cur.execute("SELECT * FROM customers WHERE phone = ?;", (customer.phone,))
    data = cur.fetchone()

    if data is not None:
        raise HTTPException(status_code=409, detail="Customer already exists")
    
    cur.execute("INSERT INTO customers (name, phone) VALUES (?, ?);", (customer.name, customer.phone))
    return Response("Customer created", Customer(id=cur.lastrowid, name=customer.name, phone=customer.phone), 201)

@app.put("/customers/{id}", tags=["Customers"])
async def update_customer(id: int, customer: Customer, cur: sqlite3.Cursor = Depends(get_db_cursor)):
    cur.execute("SELECT * FROM customers WHERE id = ?;", (id,))
    data = cur.fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    cur.execute("UPDATE customers SET name = ?, phone = ? WHERE id = ?;", (customer.name, customer.phone, id))
    return Response("Customer updated", Customer(id=id, name=customer.name, phone=customer.phone), 200)

@app.delete("/customers/{id}", tags=["Customers"])
async def delete_customer(id: int, cur: sqlite3.Cursor = Depends(get_db_cursor)):
    cur.execute("SELECT * FROM customers WHERE id = ?;", (id,))
    data = cur.fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    cur.execute("DELETE FROM customers WHERE id = ?;", (id,))
    return Response("Customer deleted", None, 200)

@app.get("/items/{id}", tags=["Items"])
async def get_item(id: int, cur: sqlite3.Cursor = Depends(get_db_cursor)):
    cur.execute("SELECT * FROM items WHERE id = ?;", (id,))
    data = cur.fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return Response("Item found", Item(id=data[0], name=data[1], price=data[2]), 200)

@app.post("/items", tags=["Items"])
async def create_item(item: Item, cur: sqlite3.Cursor = Depends(get_db_cursor)):
    cur.execute("SELECT * FROM items WHERE name = ?;", (item.name,))
    data = cur.fetchone()

    if data is not None:
        raise HTTPException(status_code=409, detail="Item already exists")
    
    cur.execute("INSERT INTO items (name, price) VALUES (?, ?);", (item.name, item.price))
    return Response("Item created", Item(id=cur.lastrowid, name=item.name, price=item.price), 201)

@app.put("/items/{id}", tags=["Items"])
async def update_item(id: int, item: Item, cur: sqlite3.Cursor = Depends(get_db_cursor)):
    cur.execute("SELECT * FROM items WHERE id = ?;", (id,))
    data = cur.fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    cur.execute("UPDATE items SET name = ?, price = ? WHERE id = ?;", (item.name, item.price, id))
    return Response("Item updated", Item(id=id, name=item.name, price=item.price), 200)

@app.delete("/items/{id}", tags=["Items"])
async def delete_item(id: int, cur: sqlite3.Cursor = Depends(get_db_cursor)):
    cur.execute("SELECT * FROM items WHERE id = ?;", (id,))
    data = cur.fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    cur.execute("DELETE FROM items WHERE id = ?;", (id,))
    return Response("Item deleted", None, 200)

@app.get("/orders/{id}", tags=["Orders"])
async def get_order(id: int, cur: sqlite3.Cursor = Depends(get_db_cursor)):
    cur.execute("SELECT * FROM orders WHERE id = ?;", (id,))
    data = cur.fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    cur.execute("SELECT items.id, items.name, items.price FROM items JOIN item_list ON items.id = item_list.item_id WHERE item_list.order_id = ?;", (id,))
    items = cur.fetchall()
    items = [Item(id=item[0], name=item[1], price=item[2]) for item in items]
    total = sum([item.price for item in items])
    
    return Response("Order found", OrderDetails(id=data[0], timestamp=data[1], cust_id=data[2], notes=data[3], itemDetails=items, total=total), 200)

@app.post("/orders", tags=["Orders"])
async def create_order(order: Order, cur: sqlite3.Cursor = Depends(get_db_cursor)):
    cur.execute("SELECT * FROM customers WHERE id = ?;", (order.cust_id,))
    data = cur.fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    cur.execute("INSERT INTO orders (cust_id, notes) VALUES (?, ?);", (order.cust_id, order.notes))
    order_id = cur.lastrowid

    for item in order.items:
        cur.execute("SELECT * FROM items WHERE id = ?;", (item,))
        data = cur.fetchone()

        if data is None:
            raise HTTPException(status_code=404, detail="Item not found")
        
        cur.execute("INSERT INTO item_list (order_id, item_id) VALUES (?, ?);", (order_id, item))
    
    return Response("Order created", Order(id=order_id, cust_id=order.cust_id, notes=order.notes, items=order.items), 201)

@app.put("/orders/{id}", tags=["Orders"])
async def update_order(id: int, order: Order, cur: sqlite3.Cursor = Depends(get_db_cursor)):
    cur.execute("SELECT * FROM orders WHERE id = ?;", (id,))
    data = cur.fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    cur.execute("UPDATE orders SET cust_id = ?, notes = ? WHERE id = ?;", (order.cust_id, order.notes, id))

    cur.execute("SELECT item_id FROM item_list WHERE order_id = ?;", (id,))
    items = cur.fetchall()
    items = [item[0] for item in items]

    for item in order.items:
        if item not in items:
            cur.execute("INSERT INTO item_list (order_id, item_id) VALUES (?, ?);", (id, item))

    for item in items:
        if item not in order.items:
            cur.execute("DELETE FROM item_list WHERE order_id = ? AND item_id = ?;", (id, item))
            
    return Response("Order updated", Order(id=id, cust_id=order.cust_id, notes=order.notes, items=order.items), 200)

@app.delete("/orders/{id}", tags=["Orders"])
async def delete_order(id: int, cur: sqlite3.Cursor = Depends(get_db_cursor)):
    cur.execute("SELECT * FROM orders WHERE id = ?;", (id,))
    data = cur.fetchone()

    if data is None:
        raise HTTPException(status_code=404, detail="Order not found")
    
    cur.execute("DELETE FROM orders WHERE id = ?;", (id,))
    cur.execute("DELETE FROM item_list WHERE order_id = ?;", (id,))
    return Response("Order deleted", None, 200)