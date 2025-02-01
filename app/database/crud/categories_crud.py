from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session
from slugify import slugify

from app.models import Category


async def select_all_active_categories(session: Session):
    query = select(Category) \
        .where(Category.is_active == True)
    return session.scalars(query).all()

async def select_category_by_id(session: Session, category_id: int):
    return session.scalar(
        select(Category).where(Category.id == category_id)
    )

async def insert_category(session: Session, **values: dict):
    query = insert(Category).values(
        slug = slugify(values["name"]),
        **values
    )
    session.execute(query)
    session.commit()

async def update_category(session: Session, category_id: int, **values: dict):
    update_values = dict(**values)
    if "name" in values:
        update_values["slug"] = slugify(values["name"])

    query = update(Category) \
        .where(Category.id == category_id) \
        .values(**update_values)
    session.execute(query)
    session.commit()

