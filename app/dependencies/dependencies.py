from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.crud import CrudManager, CategoryCrudManager, ProductCrudManager, UserCrudManager
from app.schemas import CreateUser


session_dependency = Annotated[AsyncSession, Depends(get_db_session)]
class _CheckerExistsByID:
    def __init__(self, crud_manager: CrudManager):
        self.crud_manager = crud_manager

    async def __call__(
        self,
        session: session_dependency,
        id: int
    ):
        value = await self.crud_manager.select_by_id(session, id)
        if value is None:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"There are no {self.crud_manager.model_name} found")

check_category_exists = _CheckerExistsByID(CategoryCrudManager)
check_product_exists = _CheckerExistsByID(ProductCrudManager)
check_user_exists = _CheckerExistsByID(UserCrudManager)

async def check_user_by_username_or_email(
    session: session_dependency,
    user: CreateUser
):
    checked_user = await UserCrudManager.select_by_username_or_email(session, user)
    if not checked_user is None:
        raise HTTPException(status.HTTP_409_CONFLICT, "User with this username or email already exists")