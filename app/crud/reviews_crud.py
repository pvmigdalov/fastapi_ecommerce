from uuid import UUID
from typing import Any, Mapping, Sequence

from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.reviews import UserReviewAboutProductAlreadyExistsException
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

    @classmethod
    async def select_user_review_about_product(
        cls, session: AsyncSession, user_id: UUID, product_id: UUID
    ) -> Review | None:
        reviews = await cls.select(session, user_id=user_id, product_id=product_id)
        if reviews:
            reviews[0]

    @classmethod
    async def update(
        cls,
        session: AsyncSession,
        obj: Review,
        values: Mapping[str, Any],
        commit: bool = True,
    ) -> None:
        user_review = await cls.select_user_review_about_product(
            session, obj.user_id, obj.product_id
        )
        if user_review:
            raise UserReviewAboutProductAlreadyExistsException(status_code=400)
        await super().update(session, obj, values)
