from decimal import Decimal
from enum import Enum
from typing import Annotated

from pydantic import UUID4, AnyHttpUrl, BaseModel, ConfigDict, EmailStr, Field


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

    name: Annotated[
        str, Field(..., min_length=3, max_length=100, description="Product's name")
    ]
    description: Annotated[
        str, Field("", max_length=500, description="Product's description")
    ]
    price: Annotated[
        Decimal, Field(..., gt=0, decimal_places=2, description="Product's price")
    ]
    image_url: Annotated[AnyHttpUrl, Field(..., description="Image's url")]
    stock: Annotated[int, Field(0, description="Product's stock")]
    category_id: Annotated[UUID4, Field(..., description="Category uuid v4")]
    supplier_id: Annotated[UUID4 | None, Field(None, description="Supplier's uuid v4")]


class Product(ProductCreate):
    """
    Product's schema for GET requests
    """

    id: Annotated[UUID4, Field(..., description="Product's uuid v4")]
    is_active: Annotated[bool, Field(..., description="Activity status")]
    slug: Annotated[str, Field(..., description="Product's slug")]
    rating: Annotated[float, Field(0, description="Product's rating")]

    model_config = ConfigDict(from_attributes=True)


class CreateCategory(BaseModel):
    """
    Categorie's schema for POST/PUT requests
    """

    name: Annotated[
        str, Field(..., min_length=1, max_length=250, description="Category name")
    ]
    parent_id: Annotated[
        UUID4 | None, Field(None, description="Category parent UUID4 v4")
    ]


class Category(CreateCategory):
    """
    Category schema for GET requests
    """

    id: Annotated[UUID4, Field(..., description="Category uuid v4")]
    is_active: Annotated[bool, Field(..., description="Activity status")]
    slug: Annotated[str, Field(..., description="Category slug")]

    model_config = ConfigDict(from_attributes=True)


class CreateUser(BaseModel):
    """
    User's schema for POST/PUT requests
    """

    name: str
    username: str
    email: EmailStr
    password: str
    user_role: UserRole = UserRole.CUSTOMER


class CreateUserWithHashedPassword(BaseModel):
    """
    User's schema for POST/PUT requests with hashed password
    """

    name: str
    username: str
    email: EmailStr
    hashed_password: str
    user_role: UserRole


class User(BaseModel):
    """
    User's schema for GET requests
    """

    id: Annotated[UUID4, Field(..., description="User uuid v4")]
    name: str
    username: str
    email: EmailStr
    user_role: UserRole

    model_config = ConfigDict(from_attributes=True)
