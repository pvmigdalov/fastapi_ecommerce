from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import BaseCrudManager
from app.models import Category


class CategoryCrudManager(BaseCrudManager[Category]):
    Model = Category

    @classmethod
    async def select_all_active(cls, session: AsyncSession) -> Sequence[Category]:
        return await cls.select(session)

    @classmethod
    async def get_hierarchy_ids(
        cls, session: AsyncSession, slug: str
    ) -> Sequence[UUID]:
        category_by_slug = select(Category.id).where(Category.slug == slug)

        categories_tree = category_by_slug.cte(name="categories_tree", recursive=True)
        children = select(Category.id).join(
            categories_tree, Category.parent_id == categories_tree.c.id
        )
        categories_tree = categories_tree.union_all(children)
        result = await session.scalars(select(categories_tree.c.id))

        return result.all()
