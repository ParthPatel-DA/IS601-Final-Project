from fastapi import FastAPI, Depends
from fastapi.exceptions import HTTPException
import sqlite3
from schemas import Customer, Item

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

