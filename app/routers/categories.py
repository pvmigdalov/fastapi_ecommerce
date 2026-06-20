from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, status

from app.crud import CategoryCrudManager
from app.dependencies import check_category_exists, session_dependency
from app.schemas import Category, CreateCategory

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=Sequence[Category])
async def get_all_categories(session: session_dependency):
    return await CategoryCrudManager.select_all_active(session)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Category)
async def create_category(session: session_dependency, category: CreateCategory):
    if category.parent_id:
        await check_category_exists(session, category.parent_id)
    return await CategoryCrudManager.insert(session, category)


@router.put("/", response_model=Category)
async def update_category(
    session: session_dependency, id: UUID, category_update: CreateCategory
):
    category = await check_category_exists(session, id)
    if category_update.parent_id:
        await check_category_exists(session, category_update.parent_id)
    await CategoryCrudManager.update(session, id, **category_update.model_dump())
    await session.refresh(category)
    return category


@router.delete("/", dependencies=[Depends(check_category_exists)])
async def delete_category(session: session_dependency, id: UUID):
    await CategoryCrudManager.update(session, id, is_active=False)
    return {"transaction": "Category delete is successful"}
