import uuid
from typing import TYPE_CHECKING

from sqlalchemy import (
    ForeignKey,
    Index,
    String,
    CheckConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models import Product, User


class Review(Base):
    __tablename__ = "reviews"

    product_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("products.id"), nullable=False
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False
    )
    comment: Mapped[str] = mapped_column(String(5000), nullable=False)
    grade: Mapped[int] = mapped_column(nullable=False)

    product: Mapped["Product"] = relationship("Product", back_populates="reviews")
    user: Mapped["User"] = relationship("User", back_populates="reviews")

    __table_args__ = (
        Index(
            "ix_uq_product_user_active",
            "product_id",
            "user_id",
            unique=True,
            postgresql_where="is_active = true",
        ),
        CheckConstraint("grade BETWEEN 1 AND 5", name="check_grade_range"),
    )
