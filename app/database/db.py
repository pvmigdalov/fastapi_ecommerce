import os
import uuid

from dotenv import load_dotenv
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

load_dotenv("app/settings/db.env")
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_async_engine(DATABASE_URL, echo=True)  # pyright: ignore
Session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_db_session():
    async with Session() as session:
        yield session


class Base(DeclarativeBase):
    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(default=True)
