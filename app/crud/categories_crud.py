from collections.abc import Mapping, Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.categories import FindCycleParentsCategoryException
from app.models import Category

from .crud import BaseCrudManager


class CategoryCrudManager(BaseCrudManager[Category]):
    Model = Category

    @classmethod
    async def select_all_active(cls, session: AsyncSession) -> Sequence[Category]:
        return await cls.select(session)

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        obj: Category,
        values: Mapping[str, Any],
        commit: bool = True,
    ) -> None:
        if "parent_id" in values:
            await cls.check_cycle_parents(session, obj.id, values["parent_id"])
        await super().update(session, obj, values)

    @classmethod
    async def check_cycle_parents(
        cls, session: AsyncSession, category_id: UUID, new_parent_id: UUID
    ) -> None:
        category_hierarchy_ids = await cls.get_hierarchy_ids(
            session, category_id=category_id
        )
        if new_parent_id in category_hierarchy_ids:
            raise FindCycleParentsCategoryException(status_code=400)

    @classmethod
    async def get_hierarchy_ids(
        cls,
        session: AsyncSession,
        *,
        slug: str | None = None,
        category_id: UUID | None = None,
    ) -> Sequence[UUID]:
        if slug is None and category_id is None:
            return []
        elif category_id is not None:
            category_by_cond = select(Category.id).where(Category.id == category_id)
        else:
            category_by_cond = select(Category.id).where(Category.slug == slug)

        categories_tree = category_by_cond.cte(name="categories_tree", recursive=True)
        children = select(Category.id).join(
            categories_tree, Category.parent_id == categories_tree.c.id
        )
        categories_tree = categories_tree.union_all(children)
        result = await session.scalars(select(categories_tree.c.id))

        return result.all()
