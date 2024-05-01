from pydantic import BaseModel

class Customer(BaseModel):
    id: int | None = None
    name: str
    phone: str

class Item(BaseModel):
    id: int | None = None
    name: str
    price: float

class Order(BaseModel):
    id: int | None = None
    cust_id: int
    notes: str
    items: list[int]

class OrderDetails(BaseModel):
    id: int | None = None
    timestamp: str
    cust_id: int
    notes: str
    itemDetails: list[Item] | None = []
    total: float | None = None

class ItemList(BaseModel):
    order_id: int
    item_id: int
