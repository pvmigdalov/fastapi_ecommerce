import enum

from sqlalchemy import Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    SUPPLIER = "SUPPLIER"
    CUSTOMER = "CUSTOMER"


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

    products: Mapped[list["Product"]] = relationship(
        "Product", uselist=True, back_populates="user"
    )
