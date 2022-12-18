from enum import unique
from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, func, TIMESTAMP
from sqlalchemy.dialects import postgresql

from sqlalchemy.orm import relationship

from Database.database import Base

from passlib import hash

class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String)
    name = Column(String, nullable=False)
    avatar = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    def verify_password(self, password):
        return hash.bcrypt.verify(password, self.password)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String)
    name = Column(String, nullable=False)
    phone = Column(String, unique=True)
    address = Column(String)
    avatar = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

    def verify_password(self, password):
        return hash.bcrypt.verify(password, self.password)

class Category(Base):
    __tablename__ = "category"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    image_review = Column(String)
    created_by = Column(String, ForeignKey("admin.email"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_by = Column(String, ForeignKey("admin.email"))
    updated_at = Column(TIMESTAMP, onupdate=func.now())

class Product(Base):
    __tablename__ = "product"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    images = Column(postgresql.ARRAY(String))
    size = Column(postgresql.ARRAY(String))
    price = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    description = Column(String)
    category_id = Column(Integer, ForeignKey("category.id"))
    created_by = Column(String, ForeignKey("admin.email"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_by = Column(String, ForeignKey("admin.email"))
    updated_at = Column(TIMESTAMP, onupdate=func.now())


class Cart(Base):
    __tablename__ = "cart"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    product_size = Column(String)
    quantity = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, onupdate=func.now())

class Payment(Base):
    __tablename__ = "payment"
    id = Column(Integer, primary_key=True)
    payment_method = Column(String, nullable=False)
    image_review = Column(String)
    created_by = Column(String, ForeignKey("admin.email"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_by = Column(String, ForeignKey("admin.email"))
    updated_at = Column(TIMESTAMP, onupdate=func.now())

class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_by = Column(String, ForeignKey("admin.email"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_by = Column(String, ForeignKey("admin.email"))
    updated_at = Column(TIMESTAMP, onupdate=func.now())
class Order(Base):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    products = Column(postgresql.JSONB)
    total_price = Column(Integer, nullable=False)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    note = Column(String)
    payment_id = Column(Integer, ForeignKey("payment.id"))
    status = Column(Integer, ForeignKey("status.id"))
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_by = Column(String, ForeignKey("admin.email"))
    updated_at = Column(TIMESTAMP, onupdate=func.now())
    






    