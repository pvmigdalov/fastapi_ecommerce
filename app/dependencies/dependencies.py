from asyncio import iscoroutinefunction
from functools import partial
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.crud import CategoryCrudManager, ProductCrudManager


async def check_category_exists(
    session: Annotated[AsyncSession, Depends(get_db_session)], 
    category_id: int
):
    category = await CategoryCrudManager.select_by_id(session, category_id)
    if category is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "There is no category found")
    
async def check_product_exists(
    session: Annotated[AsyncSession, Depends(get_db_session)], 
    product_id: int
):
    product = await ProductCrudManager.select_by_id(session, product_id)
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "There is no product found")