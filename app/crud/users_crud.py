from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import BaseCrudManager
from app.models import User
from app.schemas import CreateUser, CreateUserWithHashedPassword


class UserCrudManager(BaseCrudManager[User]):
    model_name = User.__tablename__
    Model = User

    @classmethod
    async def insert(  # type: ignore[override]
        cls, session: AsyncSession, schema: CreateUserWithHashedPassword
    ) -> User:
        obj = cls.Model(**schema.model_dump())
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj

    @classmethod
    async def select_by_username_or_email(
        cls, session: AsyncSession, user: CreateUser
    ) -> User | None:
        query = select(cls.Model).filter(
            (cls.Model.username == user.username) | (cls.Model.email == user.email)
        )

        return await session.scalar(query)
