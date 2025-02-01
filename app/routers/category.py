from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy import insert
from sqlalchemy.orm import Session
from slugify import slugify

from app.database import get_db_session
from app.schemas import CreateCategory
from app.models import Category

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.get("/")
async def get_all_categories():
    pass

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
    session: Annotated[Session, Depends(get_db_session)],
    category: CreateCategory
):
    stmt = insert(Category).values(
        name=category.name,
        parent_id=category.parent_id,
        slug = slugify(category.name)
    )
    session.execute(stmt)
    session.commit()

    return {"transation": "Successful"}

@router.put("/")
async def update_category():
    pass

@router.delete("/")
async def delete_category():
    pass