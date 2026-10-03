from abc import ABC, abstractmethod
from typing import Any, Sequence
from uuid import UUID

from slugify import slugify
from sqlalchemy import insert, select, true, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base
from app.utils import classproperty


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
        res = await session.scalars(select(cls.Model).where(cls.Model.id == _id))
        return res.first()

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
    async def insert(cls, session: AsyncSession, **values: Any):
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


class AbstractCrudManager[T: Base](ABC):
    Model: type[T]

    @classmethod
    @abstractmethod
    async def add(cls, session: AsyncSession, obj: T) -> None: ...

    @classmethod
    @abstractmethod
    async def select(cls, session: AsyncSession, **conditions: Any) -> Sequence[T]: ...

    @classmethod
    @abstractmethod
    async def select_by_id(cls, session: AsyncSession, _id: UUID) -> T | None: ...

    @classmethod
    @abstractmethod
    async def update(
        cls,
        session: AsyncSession,
        obj: T,
        **values: Any,
    ) -> None: ...


class NewBaseCrudManager[T: Base](AbstractCrudManager[T]):
    Model: type[T]

    @classmethod
    async def add(cls, session: AsyncSession, obj: T) -> None:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)

    @classmethod
    async def select(cls, session: AsyncSession, **conditions: Any) -> Sequence[T]:
        conditions["is_active"] = True
        stmt = select(cls.Model).where(**conditions)
        res = await session.scalars(stmt)
        return res.all()

    @classmethod
    async def select_by_id(cls, session: AsyncSession, _id: UUID) -> T | None:
        stmt = select(cls.Model).where(
            cls.Model.id == _id, cls.Model.is_active.is_(true())
        )
        return await session.scalar(stmt)

    @classmethod
    async def update(cls, session: AsyncSession, obj: T, **values: Any) -> None:
        for k, v in values.items():
            if hasattr(obj, k):
                setattr(obj, k, v)

        await session.commit()
        await session.refresh(obj)

    @classproperty
    def model_name(cls) -> str:
        return cls.Model.__tablename__
