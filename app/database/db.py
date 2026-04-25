import os
from uuid import uuid4

from dotenv import load_dotenv
from sqlalchemy import Boolean, Column, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.dialects.postgresql import UUID

load_dotenv("app/settings/db.env")
DATABASE_URL = os.getenv("DATABASE_URL")


engine = create_async_engine(DATABASE_URL, echo=True)
Session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

async def get_db_session():
    async with Session() as session:
        yield session

class Base(DeclarativeBase):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String)
    is_active = Column(Boolean, default=True)