import uuid
from decimal import Decimal
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


if TYPE_CHECKING:
    from app.models import Category, User


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str]
    slug: Mapped[str]
    description: Mapped[str | None] = mapped_column(default=None)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=15, scale=2))
    image_url: Mapped[str | None] = mapped_column(default=None)
    stock: Mapped[int] = mapped_column(default=0)
    rating: Mapped[float] = mapped_column(default=0.0)
    category_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id")
    )
    supplier_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id")
    )

    category: Mapped["Category"] = relationship("Category", back_populates="products")
    user: Mapped["User"] = relationship("User", back_populates="products")
