from typing import Any

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import BaseCrudManager
from ..models import User
from ..schemas import CreateUser


class UserCrudManager(BaseCrudManager[User]):
    model_name = User.__tablename__
    Model = User

    @classmethod
    async def insert(cls, session: AsyncSession, **values: Any) -> None:
        query = insert(cls.Model).values(**values)

        await session.execute(query)
        await session.commit()

    @classmethod
    async def select_by_username_or_email(
        cls, session: AsyncSession, user: CreateUser
    ) -> User | None:
        query = select(cls.Model).filter(
            (cls.Model.username == user.username) | (cls.Model.email == user.email)
        )

        return await session.scalar(query)
