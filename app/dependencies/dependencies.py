from asyncio import iscoroutinefunction
from functools import partial
from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.crud import CrudManager, CategoryCrudManager, ProductCrudManager, UserCrudManager


class _CheckerExists:
    def __init__(self, crud_manager: CrudManager):
        self.crud_manager = crud_manager

    async def __call__(
        self,
        session: Annotated[AsyncSession, Depends(get_db_session)],
        id: int
    ):
        value = await self.crud_manager.select_by_id(session, id)
        if value is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"There are no {self.crud_manager.model_name} found")

check_category_exists = _CheckerExists(CategoryCrudManager)
check_product_exists = _CheckerExists(ProductCrudManager)
check_user_exists = _CheckerExists(UserCrudManager)

# async def check_category_exists(
#     session: Annotated[AsyncSession, Depends(get_db_session)], 
#     category_id: int
# ):
#     category = await CategoryCrudManager.select_by_id(session, category_id)
#     if category is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, "There is no category found")
    
# async def check_product_exists(
#     session: Annotated[AsyncSession, Depends(get_db_session)], 
#     product_id: int
# ):
#     product = await ProductCrudManager.select_by_id(session, product_id)
#     if product is None:
#         raise HTTPException(status.HTTP_404_NOT_FOUND, "There is no product found")