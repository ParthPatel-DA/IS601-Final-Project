from pydantic import BaseModel

class Customer(BaseModel):
    id: int | None = None
    name: str
    phone: str

class Item(BaseModel):
    id: int | None = None
    name: str
    price: float
