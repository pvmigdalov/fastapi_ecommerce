import enum
from typing import TYPE_CHECKING

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


if TYPE_CHECKING:
    from app.models import Product, Review


class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    SUPPLIER = "SUPPLIER"
    CUSTOMER = "CUSTOMER"


class User(Base):
    __tablename__ = "users"

    name: Mapped[str]
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    user_role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.CUSTOMER,
        server_default=UserRole.CUSTOMER.value,
        nullable=False,
    )

    products: Mapped[list["Product"]] = relationship("Product", back_populates="user")
    reviews: Mapped[list["Review"]] = relationship("Review", back_populates="user")
