import enum

from sqlalchemy import Boolean, Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class UserRole(enum.Enum):
    ADMIN = "admin"
    SUPPLIER = "supplier"
    CUSTOMER = "customer"

class Category(Base):
    __tablename__ = "categories"

    slug = Column(String, unique=True, index=True)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    
    products = relationship("Product", back_populates="category")

class Product(Base):
    __tablename__ = "products"

    slug = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Integer)
    image_url = Column(String)
    stock = Column(Integer)
    rating = Column(Float)
    category_id = Column(Integer, ForeignKey("categories.id"))
    supplier_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    category = relationship("Category", back_populates="products")
    user = relationship("User", back_populates="products")

class User(Base):
    __tablename__ = "users"

    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    is_admin = Column(Boolean, default=False)
    is_supplier = Column(Boolean, default=False)
    is_customer = Column(Boolean, default=True)
    user_role = Column(Enum(UserRole), default=UserRole.CUSTOMER, server_default=UserRole.CUSTOMER.value, nullable=False)

    products = relationship("Product", back_populates="user")