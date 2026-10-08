from uuid import UUID
from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Review
from .crud import BaseCrudManager


class ReviewCrudManager(BaseCrudManager[Review]):
    Model = Review

    @classmethod
    async def select_all_active(cls, session: AsyncSession) -> Sequence[Review]:
        return await cls.select(session)

    @classmethod
    async def select_product_reviews(
        cls, session: AsyncSession, product_id: UUID
    ) -> Sequence[Review]:
        return await cls.select(session, product_id=product_id)
