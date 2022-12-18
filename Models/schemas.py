from pydantic import BaseModel


class User(BaseModel):
    email: str
    password: str
    name: str
    phone: str
    address: str
    avatar: str


class Admin(BaseModel):
    email: str
    password: str
    name: str
    avatar: str

class AdminUpdate(BaseModel):
    email: str
    name: str
    avatar: str

class Category(BaseModel):
    name: str
    image_review: str


class Product(BaseModel):
    name: str
    images: list
    size: list
    price: int
    description: str
    quantity: int
    category_id: int


class Cart(BaseModel):
    product_id: int
    product_size: str
    quantity: int


class Status(BaseModel):
    name: str


class Order(BaseModel):
    products: list
    total_price: int
    name: str
    email: str
    address: str
    phone: str
    note: str
    status: int
    payment_id: int


class Payment(BaseModel):
    payment_method: str
    image_review: str
