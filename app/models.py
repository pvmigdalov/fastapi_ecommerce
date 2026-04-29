import enum

from sqlalchemy import Column, Enum, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from .database import Base


class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    SUPPLIER = "SUPPLIER"
    CUSTOMER = "CUSTOMER"
    
class Category(Base):
    __tablename__ = "categories"

    slug = Column(String, unique=True, index=True)
    parent_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True)
    
    products = relationship("Product", uselist=True, back_populates="category")

class Product(Base):
    __tablename__ = "products"

    slug = Column(String, unique=True, index=True)
    description = Column(String)
    price = Column(Float)
    image_url = Column(String)
    stock = Column(Integer)
    rating = Column(Float, default=0)
    category_id = Column(UUID(as_uuid=True), ForeignKey("categories.id"))
    supplier_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)

    category = relationship("Category", back_populates="products")
    user = relationship("User", back_populates="products")

class User(Base):
    __tablename__ = "users"

    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashed_password = Column(String)
    # is_admin = Column(Boolean, default=False)
    # is_supplier = Column(Boolean, default=False)
    # is_customer = Column(Boolean, default=True)
    user_role = Column(
        Enum(UserRole), 
        default=UserRole.CUSTOMER, 
        server_default=UserRole.CUSTOMER.value, 
        nullable=False
    )

    products = relationship("Product", uselist=True, back_populates="user")