from uuid import UUID
from typing import Sequence, Any

from slugify import slugify
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import BaseCrudManager
from app.crud import CategoryCrudManager
from app.models import Product
from app.schemas import ProductCreate


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

    @classmethod
    async def insert(
        cls, session: AsyncSession, schema: ProductCreate, supplier_id: UUID
    ) -> Product:  # type: ignore[override]  # ty: ignore[invalid-method-override]
        fields = schema.model_dump()
        if "name" in fields:
            fields["slug"] = slugify(fields["name"])

        product = cls.Model(**fields, supplier_id=supplier_id)
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        product: Product,
        **values: Any,
    ) -> None:  # ty: ignore[invalid-method-override]
        updates = dict(**values)
        if "name" in updates:
            updates["slug"] = slugify(updates["name"])

        for k, v in updates.items():
            setattr(product, k, v)
        await session.commit()
        await session.refresh(product)
