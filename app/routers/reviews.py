from typing import Annotated
from collections.abc import Sequence

from fastapi import APIRouter, Depends

from app.crud import ReviewCrudManager
from app.dependencies import session_dependency, get_owned_review
from app.schemas.reviews import Review, ReviewUpdate
from app.models import Review as ReviewModel


router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.get("/", response_model=Sequence[Review])
async def get_all_reviews(session: session_dependency):
    return await ReviewCrudManager.select_all_active(session)


@router.put("/{review_id:uuid}", response_model=Review)
async def update_review(
    session: session_dependency,
    review: Annotated[ReviewModel, Depends(get_owned_review)],
    review_update: ReviewUpdate,
):
    updates = review_update.model_dump(exclude_none=True)
    await ReviewCrudManager.update(session, review, updates)
    return review


@router.delete("/{review_id:uuid}")
async def delete_review(
    session: session_dependency,
    review: Annotated[ReviewModel, Depends(get_owned_review)],
):
    await ReviewCrudManager.delete(session, review)
    return {"transaction": "Review delete is successful"}
