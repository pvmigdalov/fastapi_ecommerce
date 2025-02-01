from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session
from slugify import slugify

from app.database import Base


class CrudManager:
    Model: type[Base]

    @classmethod    
    async def select_all_active(cls, session: Session):
        query = select(cls.Model) \
            .where(cls.Model.is_active == True)
        return session.scalars(query).all()
    
    @classmethod
    async def select_by_id(cls, session: Session, _id: int):
        return session.scalar(
            select(cls.Model).where(cls.Model.id == _id)
        )
    
    @classmethod
    async def insert(cls, session: Session, **values: dict):
        query = insert(cls.Model).values(
            slug = slugify(values["name"]),
            **values
        )
        session.execute(query)
        session.commit()
    
    @classmethod
    async def update(cls, session: Session, _id: int, **values: dict):
        update_values = dict(**values)
        if "name" in values:
            update_values["slug"] = slugify(values["name"])

        query = update(cls.Model) \
            .where(cls.Model.id == _id) \
            .values(**update_values)
        session.execute(query)
        session.commit()