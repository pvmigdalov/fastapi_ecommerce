from typing import Any

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import CrudManager
from app.models import User


class UserCrudManager(CrudManager):
    model_name = "users"
    Model = User

    @classmethod
    async def insert(cls, session: AsyncSession, **values: dict[str, Any]):
        query = insert(cls.Model).values(**values)
        
        await session.execute(query)
        await session.commit()