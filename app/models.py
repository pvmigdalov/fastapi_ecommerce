import enum
import uuid
from decimal import Decimal

from sqlalchemy import Enum, ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .database import Base


class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    SUPPLIER = "SUPPLIER"
    CUSTOMER = "CUSTOMER"


class Category(Base):
    __tablename__ = "categories"

    slug: Mapped[str] = mapped_column(unique=True, index=True)
    parent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True
    )

    products = relationship("Product", uselist=True, back_populates="category")


class Product(Base):
    __tablename__ = "products"

    slug: Mapped[str] = mapped_column(unique=True, index=True)
    description: Mapped[str] = mapped_column()
    price: Mapped[Decimal] = mapped_column(Numeric(precision=15, scale=2))
    image_url: Mapped[str] = mapped_column()
    stock: Mapped[int] = mapped_column()
    rating: Mapped[float] = mapped_column(default=0.0)
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id")
    )
    supplier_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=True
    )

    category = relationship("Category", back_populates="products")
    user = relationship("User", back_populates="products")


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    hashed_password: Mapped[str] = mapped_column()
    user_role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        default=UserRole.CUSTOMER,
        server_default=UserRole.CUSTOMER.value,
        nullable=False,
    )

    products = relationship("Product", uselist=True, back_populates="user")
