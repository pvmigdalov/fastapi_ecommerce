from typing import Sequence

from slugify import slugify
from sqlalchemy import select, union
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import BaseCrudManager
from app.models import Category, Product
from app.schemas import ProductCreate


class ProductCrudManager(BaseCrudManager[Product]):
    model_name = Product.__tablename__
    Model = Product

    @classmethod
    async def select_all_active(cls, session: AsyncSession) -> Sequence[Product]:
        query = select(cls.Model).where(cls.Model.is_active, cls.Model.stock > 0)
        result = await session.scalars(query)
        return result.all()

    @classmethod
    async def select_products_by_category(
        cls, session: AsyncSession, category_slug: str
    ) -> Sequence[Product]:
        category_by_slug = (
            select(Category.id).where(Category.slug == category_slug).cte()
        )

        category_hierarchy = union(
            select(category_by_slug.c.id),
            select(Category.id).join(
                category_by_slug, Category.parent_id == category_by_slug.c.id
            ),
        ).cte()

        query = select(cls.Model).join(
            category_hierarchy, cls.Model.category_id == category_hierarchy.c.id
        )

        result = await session.scalars(query)
        return result.all()

    @classmethod
    async def insert(cls, session: AsyncSession, schema: ProductCreate) -> Product:  # type: ignore[override]
        fields = schema.model_dump()
        obj = cls.Model(slug=slugify(fields["name"]), **fields)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
