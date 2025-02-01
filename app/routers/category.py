from typing import Annotated

from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy import insert, select, update
from sqlalchemy.orm import Session
from slugify import slugify

from app.database import get_db_session
from app.schemas import CreateCategory
from app.models import Category

router = APIRouter(prefix="/categories", tags=["Categories"])

# general annotations
session_dependency = Annotated[Session, Depends(get_db_session)]

@router.get("/")
async def get_all_categories(session: session_dependency):
    query = select(Category) \
        .where(Category.is_active == True)
    return session.scalars(query).all()

@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_category(
    session: session_dependency,
    category: CreateCategory
):
    query = insert(Category).values(
        name=category.name,
        parent_id=category.parent_id,
        slug = slugify(category.name)
    )
    session.execute(query)
    session.commit()

    return {"transaction": "Successful"}

@router.put("/")
async def update_category(
    session: session_dependency, 
    category_id: int, 
    category_update: CreateCategory
):
    category = session.scalar(
        select(Category).where(Category.id == category_id)
    )
    if category is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "There is no category found")
    
    query = update(Category) \
        .where(Category.id == category_id) \
        .values(
            slug=slugify(category_update.name), 
            **category_update.model_dump()
        )
    session.execute(query)
    session.commit()

    return {
        "transaction": "Category update is successful"
    }

@router.delete("/")
async def delete_category(session: session_dependency, category_id: int):
    category = session.scalar(
        select(Category).where(Category.id == category_id)
    )
    if category is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "There is no category found")
    
    query = update(Category) \
        .where(Category.id == category_id) \
        .values(is_active=False)
    session.execute(query)
    session.commit()

    return {"transaction": "Category delete is successful"}