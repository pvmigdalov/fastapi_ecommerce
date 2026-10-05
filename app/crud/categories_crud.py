from collections.abc import Sequence
from uuid import UUID

from sqlalchemy import select, union_all
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import BaseCrudManager
from app.models import Category


class CategoryCrudManager(BaseCrudManager[Category]):
    Model = Category

    @classmethod
    async def get_hierarchy_ids(
        cls, session: AsyncSession, slug: str
    ) -> Sequence[UUID]:
        category_by_slug = select(Category.id).where(Category.slug == slug)

        recursive_alias = category_by_slug.cte(name="category_tree", recursive=True)
        children_query = select(Category.id).join(
            recursive_alias, Category.parent_id == recursive_alias.c.id
        )

        tree_query = union_all(category_by_slug, children_query)
        result = await session.scalars(tree_query)

        return result.all()
