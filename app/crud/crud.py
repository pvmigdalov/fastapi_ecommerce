from abc import ABC, abstractmethod
from typing import Any, Sequence
from uuid import UUID

from sqlalchemy import select, true
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import Base
from app.utils import classproperty


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


class BaseCrudManager[T: Base](AbstractCrudManager[T]):
    Model: type[T]

    @classmethod
    async def add(cls, session: AsyncSession, obj: T) -> None:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)

    @classmethod
    async def select(
        cls, session: AsyncSession, is_active: bool = True, **conditions: Any
    ) -> Sequence[T]:
        stmt = select(cls.Model).where(cls.Model.is_active == is_active)
        for column_name, value in conditions.items():
            if column := getattr(cls.Model, column_name, None):
                stmt = stmt.where(column == value)
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
