from gettext import Catalog
from typing import Sequence
from uuid import UUID

from fastapi import APIRouter, Depends, status

from ..crud import CategoryCrudManager
from ..dependencies import check_category_exists, session_dependency
from ..schemas import Category, CreateCategory

router = APIRouter(prefix="/categories", tags=["Categories"])

# session_dependency = Annotated[AsyncSession, Depends(get_db_session)]


@router.get("/")
async def get_all_categories(session: session_dependency) -> Sequence[Category]:
    categories = await CategoryCrudManager.select_all_active(session)
    return [Category.model_validate(category) for category in categories]


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
    session: session_dependency, category: CreateCategory
) -> CreateCategory:
    await CategoryCrudManager.insert(session, **category.model_dump())
    return category


@router.put("/", dependencies=[Depends(check_category_exists)])
async def update_category(
    session: session_dependency, id: UUID, category_update: CreateCategory
) -> CreateCategory:
    await CategoryCrudManager.update(session, id, **category_update.model_dump())
    return category_update


@router.delete("/", dependencies=[Depends(check_category_exists)])
async def delete_category(session: session_dependency, id: UUID):
    await CategoryCrudManager.update(session, id, is_active=False)
    return {"transaction": "Category delete is successful"}
