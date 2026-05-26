from typing import Any, Sequence
from uuid import UUID

from slugify import slugify
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import Base


class BaseCrudManager[T: Base]:
    model_name: str
    Model: type[T]

    @classmethod
    async def select_all_active(cls, session: AsyncSession) -> Sequence[T]:
        query = select(cls.Model).where(cls.Model.is_active)
        result = await session.scalars(query)
        return result.all()

    @classmethod
    async def select_by_id(cls, session: AsyncSession, _id: UUID) -> T | None:
        return await session.scalar(select(cls.Model).where(cls.Model.id == _id))

    @classmethod
    async def select_by_condition(
        cls, session: AsyncSession, **conditions: Any
    ) -> T | None:
        query = select(cls.Model)
        for column_name, value in conditions.items():
            if column := getattr(cls.Model, column_name, None):
                query = query.where(column == value)
            else:
                return None

        return await session.scalar(query)

    @classmethod
    async def insert(cls, session: AsyncSession, **values: Any) -> None:
        query = insert(cls.Model).values(slug=slugify(values["name"]), **values)
        await session.execute(query)
        await session.commit()

    @classmethod
    async def update(cls, session: AsyncSession, _id: UUID, **values: Any) -> None:
        update_values = dict(**values)
        if "name" in values:
            update_values["slug"] = slugify(values["name"])

        query = update(cls.Model).where(cls.Model.id == _id).values(**update_values)
        await session.execute(query)
        await session.commit()
