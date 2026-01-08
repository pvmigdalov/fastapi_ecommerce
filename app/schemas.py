from decimal import Decimal
from enum import Enum
from typing import Annotated

from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserRole(str, Enum):
    """
    Enum of user roles without admin role
    """
    SUPPLIER = "SUPPLIER"
    CUSTOMER = "CUSTOMER"    


class ProductCreate(BaseModel):
    """
    Product's schema for POST/PUT requests
    """
    name: Annotated[str, Field(..., min_length=3, max_length=100, description="")]
    description: str
    price: int
    image_url: str
    stock: int
    category_id: int

class Product(ProductCreate):
    """
    Product's schema for GET requests
    """
    pass

class CreateCategory(BaseModel):
    name: str
    parent_id: int | None = None

class CreateUser(BaseModel):
    name: str
    username: str
    email: EmailStr
    password: str
    user_role: UserRole = UserRole.CUSTOMER