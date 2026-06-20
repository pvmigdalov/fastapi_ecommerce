from typing import Annotated, NoReturn
from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import (
    BaseCrudManager,
    CategoryCrudManager,
    ProductCrudManager,
    UserCrudManager,
)
from app.database import get_db_session, Base
from app.schemas import CreateUser
from app.models import Category, Product, User

session_dependency = Annotated[AsyncSession, Depends(get_db_session)]


class _CheckerExistsByID[T: Base]:
    def __init__(self, crud_manager: type[BaseCrudManager]):
        self.crud_manager = crud_manager

    async def __call__(self, session: session_dependency, id: UUID) -> T:
        value = await self.crud_manager.select_by_id(session, id)
        if value is None:
            raise HTTPException(
                status.HTTP_404_NOT_FOUND,
                f"There are no {self.crud_manager.model_name} found",
            )
        return value


check_category_exists = _CheckerExistsByID[Category](CategoryCrudManager)
check_product_exists = _CheckerExistsByID[Product](ProductCrudManager)
check_user_exists = _CheckerExistsByID[User](UserCrudManager)


async def check_user_by_username_or_email(
    session: session_dependency, user: CreateUser
) -> NoReturn | None:
    checked_user = await UserCrudManager.select_by_username_or_email(session, user)
    if checked_user is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "User with this username or email already exists"
        )
