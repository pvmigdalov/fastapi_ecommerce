from sqlalchemy import select
from sqlalchemy.orm import Session, aliased

from app.crud.crud import CrudManager
from app.models import Category, Product

class ProductCrudManager(CrudManager):
    Model = Product

    @classmethod    
    async def select_all_active(cls, session: Session):
        query = select(cls.Model) \
            .where(cls.Model.is_active == True, cls.Model.stock > 0)
        return session.scalars(query).all()
    
    @classmethod
    async def select_products_by_category(
        cls, 
        session: Session, 
        category_slug: str
    ):
        category_by_slug = select(Category.id) \
            .where(Category.slug == category_slug) \
            .subquery()
            
        query = select(cls.Model) \
            .join(category_by_slug, cls.Model.category_id == category_by_slug.columns.id)

        return session.scalars(query).all()