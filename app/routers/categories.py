from typing import Annotated, Sequence

from fastapi import APIRouter, Depends, status
from slugify import slugify

from app.crud import CategoryCrudManager
from app.dependencies import (
    check_category_exists,
    get_current_admin,
    session_dependency,
)
from app.models import Category as CategoryModel
from app.schemas import Category, CreateCategory

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=Sequence[Category])
async def get_all_categories(session: session_dependency):
    return await CategoryCrudManager.select_all_active(session)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=Category,
    dependencies=[Depends(get_current_admin)],
)
async def create_category(session: session_dependency, category: CreateCategory):
    if category.parent_id:
        await check_category_exists(session, category.parent_id)

    category_data = category.model_dump()
    new_category = CategoryModel(
        **category_data,
        slug=slugify(category_data["name"]),
    )
    await CategoryCrudManager.add(session, new_category)

    return new_category


@router.put(
    "/{id:uuid}",
    response_model=Category,
    dependencies=[Depends(get_current_admin)],
)
async def update_category(
    session: session_dependency,
    category: Annotated[CategoryModel, Depends(check_category_exists)],
    category_update: CreateCategory,
):
    updates = category_update.model_dump(exclude_none=True)
    if not updates:
        return category

    if category_update.parent_id:
        await check_category_exists(session, category_update.parent_id)

    if "name" in updates:
        updates["slug"] = slugify(updates["name"])

    await CategoryCrudManager.update(session, category, **updates)
    await session.refresh(category)
    return category


@router.delete("/{id:uuid}", dependencies=[Depends(get_current_admin)])
async def delete_category(
    session: session_dependency,
    category: Annotated[CategoryModel, Depends(check_category_exists)],
) -> dict:
    await CategoryCrudManager.delete(session, category)
    return {"transaction": "Category delete is successful"}
