from slugify import slugify
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.crud import BaseCrudManager
from app.models import Category
from app.schemas import CreateCategory


class CategoryCrudManager(BaseCrudManager[Category]):
    model_name = Category.__tablename__
    Model = Category

    @classmethod
    async def insert(cls, session: AsyncSession, schema: CreateCategory) -> Category:
        fields = schema.model_dump()
        obj = cls.Model(slug=slugify(fields["name"]), **fields)
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
