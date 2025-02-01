from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session
from slugify import slugify

from app.models import Product


async def select_all_active_products(session: Session):
    query = select(Product) \
        .where(Product.is_active == True)
    return session.scalars(query).all()