from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.crud import CategoryCrudManager
from app.schemas import CreateCategory
from app.dependencies import check_category_exists


router = APIRouter(prefix="/categories", tags=["Categories"])

session_dependency = Annotated[AsyncSession, Depends(get_db_session)]

@router.get("/")
async def get_all_categories(session: session_dependency):
    return await CategoryCrudManager.select_all_active(session)

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
    session: session_dependency,
    category: CreateCategory
):
    await CategoryCrudManager.insert(session, **category.model_dump())
    return {"transaction": "Successful"}

@router.put("/", dependencies=[Depends(check_category_exists)])
async def update_category(
    session: session_dependency,
    id: int, 
    category_update: CreateCategory
):
    await CategoryCrudManager.update(session, id, **category_update.model_dump())
    return {
        "transaction": "Category update is successful"
    }

@router.delete("/", dependencies=[Depends(check_category_exists)])
async def delete_category(
    session: session_dependency, 
    id: int
):
    await CategoryCrudManager.update(session, id, is_active=False)
    return {"transaction": "Category delete is successful"}