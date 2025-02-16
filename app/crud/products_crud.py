from sqlalchemy import select, union
from sqlalchemy.orm import Session

from app.crud.crud import CrudManager
from app.models import Category, Product

class ProductCrudManager(CrudManager):
    model_name = "products"
    Model = Product

    @classmethod    
    async def select_all_active(cls, session: Session):
        query = select(cls.Model) \
            .where(cls.Model.is_active == True, cls.Model.stock > 0)
        result = await session.scalars(query)
        return result.all()
    
    @classmethod
    async def select_products_by_category(
        cls, 
        session: Session, 
        category_slug: str
    ):
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