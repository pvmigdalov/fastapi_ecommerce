from enum import Enum
from typing import Annotated

from pydantic import UUID4, BaseModel, ConfigDict, EmailStr, Field


class UserRole(str, Enum):
    """
    Enum of user roles without admin role
    """

    SUPPLIER = "SUPPLIER"
    CUSTOMER = "CUSTOMER"


class CreateUser(BaseModel):
    """
    User's schema for POST/PUT requests
    """

    name: str
    username: str
    email: EmailStr
    password: str
    user_role: UserRole = UserRole.CUSTOMER
    model_config = ConfigDict(extra="forbid")


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
