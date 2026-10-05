from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BaseCrudManager
from app.crud import CategoryCrudManager
from app.models import Product


class ProductCrudManager(BaseCrudManager[Product]):
    Model = Product

    @classmethod
    async def select_all_active(cls, session: AsyncSession) -> Sequence[Product]:
        return await cls.select(session)

    @classmethod
    async def select_products_by_category(
        cls, session: AsyncSession, category_slug: str
    ) -> Sequence[Product]:
        category_hierarchy_ids = await CategoryCrudManager.get_hierarchy_ids(
            session, category_slug
        )
        stmt = select(cls.Model).where(
            cls.Model.category_id.in_(category_hierarchy_ids)
        )
        result = await session.scalars(stmt)

        return result.all()
