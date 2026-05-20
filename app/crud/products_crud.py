from typing import Sequence

from sqlalchemy import select, union
from sqlalchemy.ext.asyncio import AsyncSession

from .crud import BaseCrudManager
from ..models import Category, Product


class ProductCrudManager(BaseCrudManager):
    model_name = "products"
    Model = Product

    @classmethod    
    async def select_all_active(cls, session: AsyncSession) -> Sequence[Product]:
        query = select(cls.Model) \
            .where(cls.Model.is_active, cls.Model.stock > 0)
        result = await session.scalars(query)
        return result.all()
    
    @classmethod
    async def select_products_by_category(
        cls, 
        session: AsyncSession, 
        category_slug: str
    ) -> Sequence[Product]:
        category_by_slug = select(Category.id) \
            .where(Category.slug == category_slug) \
            .cte()
        
        category_hierarchy = union(
            select(category_by_slug.c.id),
            select(Category.id) \
                .join(category_by_slug, Category.parent_id == category_by_slug.c.id)
        ).cte()
            
        query = select(cls.Model) \
            .join(category_hierarchy, cls.Model.category_id == category_hierarchy.c.id)

        result = await session.scalars(query)
        return result.all()
    
# from .crud import BaseCrudManager

# class PM(BaseCrudManager[Product]):
#     @classmethod
#     async def select_all_active(cls, session: AsyncSession):
#         query = select(Product) \
#             .where(Product.is_active, Product.stock > 0)
#         result = await session.scalars(query)
#         return result.all()
    
# PM.select_all_active()