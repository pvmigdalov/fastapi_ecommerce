import uuid

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Category(Base):
    __tablename__ = "categories"

    slug: Mapped[str] = mapped_column(unique=True, index=True)
    parent_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("categories.id"), nullable=True
    )

    products: Mapped[list["Product"]] = relationship(
        "Product", back_populates="category"
    )
    children: Mapped[list["Category"]] = relationship(
        "Category", back_populates="parent"
    )
    parent: Mapped["Category | None"] = relationship(
        "Category", remote_side="Category.id", back_populates="children"
    )
