from collections.abc import Sequence
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.crud import ReviewCrudManager
from app.dependencies import (
    check_product_exists,
    get_current_customer,
    get_owned_review,
    session_dependency,
)
from app.models import Review as ReviewModel
from app.schemas.reviews import Review, ReviewCreate, ReviewUpdate

router = APIRouter(prefix="/reviews", tags=["Reviews"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Review,
    dependencies=[Depends(get_current_customer)],
)
async def create_review(
    session: session_dependency,
    review: ReviewCreate,
):
    review_data = review.model_dump(exclude_none=True)
    new_review = ReviewModel(**review_data)
    await ReviewCrudManager.add(session, new_review)
    return new_review


@router.get(
    "/product/{product_id:uuid}",
    response_model=Sequence[Review],
    dependencies=[Depends(check_product_exists)],
)
async def get_products_reviews(
    session: session_dependency,
    product_id: UUID,
):
    return await ReviewCrudManager.select_product_reviews(session, product_id)


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
