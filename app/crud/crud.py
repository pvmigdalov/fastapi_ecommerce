from typing import Any

from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from slugify import slugify

from app.database import Base


class CrudManager:
    model_name: str
    Model: type[Base]

    @classmethod    
    async def select_all_active(cls, session: AsyncSession):
        query = select(cls.Model) \
            .where(cls.Model.is_active == True)
        result = await session.scalars(query)
        return result.all()
    
    @classmethod
    async def select_by_id(cls, session: AsyncSession, _id: int):
        return await session.scalar(
            select(cls.Model).where(cls.Model.id == _id)
        )

    @classmethod
    async def select_by_condition(cls, session: AsyncSession, **conditions: dict[str, Any]):
        query = select(cls.Model)
        for column_name, value in conditions.items():
            if column := getattr(cls.Model, column_name, None):
                query = query.where(column == value)
            else:
                return None

        return await session.scalar(query)

    
    @classmethod
    async def insert(cls, session: AsyncSession, **values: dict[str, Any]):
        query = insert(cls.Model).values(
            slug = slugify(values["name"]),
            **values
        )
        await session.execute(query)
        await session.commit()
    
    @classmethod
    async def update(cls, session: AsyncSession, _id: int, **values: dict[str, Any]):
        update_values = dict(**values)
        if "name" in values:
            update_values["slug"] = slugify(values["name"])

        query = update(cls.Model) \
            .where(cls.Model.id == _id) \
            .values(**update_values)
        await session.execute(query)
        await session.commit()