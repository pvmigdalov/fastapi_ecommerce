from typing import Sequence, TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Product
from .crud import BaseCrudManager


if TYPE_CHECKING:
    from app.crud import CategoryCrudManager


class ProductCrudManager(BaseCrudManager[Product]):
    Model = Product

    @classmethod
    async def select_all_active(cls, session: AsyncSession) -> Sequence[Product]:
        return await cls.select(session)

    @classmethod
    async def select_products_by_category(
        cls,
        session: AsyncSession,
        category_slug: str,
        CategoryCM: type["CategoryCrudManager"],
    ) -> Sequence[Product]:
        category_hierarchy_ids = await CategoryCM.get_hierarchy_ids(
            session, category_slug
        )
        stmt = select(cls.Model).where(
            cls.Model.category_id.in_(category_hierarchy_ids)
        )
        result = await session.scalars(stmt)

        return result.all()
