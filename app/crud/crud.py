from abc import ABC, abstractmethod
from collections.abc import Mapping
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
        values: Mapping[str, Any],
    ) -> None: ...

    @classmethod
    @abstractmethod
    async def delete(cls, session: AsyncSession, obj: T) -> None: ...


class BaseCrudManager[T: Base](AbstractCrudManager[T]):
    Model: type[T]

    @classmethod
    async def add(cls, session: AsyncSession, obj: T, commit: bool = True) -> None:
        session.add(obj)
        if commit:
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
    async def update(
        cls,
        session: AsyncSession,
        obj: T,
        values: Mapping[str, Any],
        commit: bool = True,
    ) -> None:
        for k, v in values.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        if commit:
            await session.commit()
            await session.refresh(obj)

    @classmethod
    async def delete(cls, session: AsyncSession, obj: T) -> None:
        await cls.update(session, obj, {"is_active": False})

    @classproperty
    def model_name(cls) -> str:
        return cls.Model.__tablename__
