from sqlalchemy import select, true
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import BaseCrudManager
from app.models import User


class UserCrudManager(BaseCrudManager[User]):
    Model = User

    @classmethod
    async def select_by_username(
        cls, session: AsyncSession, username: str
    ) -> User | None:
        users = await cls.select(session, username=username)
        user = users[0] if users else None
        return user

    @classmethod
    async def select_by_username_or_email(
        cls, session: AsyncSession, username: str, email: str
    ) -> User | None:
        query = select(cls.Model).filter(
            (cls.Model.username == username) | (cls.Model.email == email),
            cls.Model.is_active.is_(true()),
        )

        return await session.scalar(query)
