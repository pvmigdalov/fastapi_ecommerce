from typing import NoReturn
from uuid import UUID

from fastapi import status

from app.crud import (
    BaseCrudManager,
    CategoryCrudManager,
    ProductCrudManager,
    ReviewCrudManager,
    UserCrudManager,
)
from app.database import Base
from app.exceptions import BaseApplicationException
from app.exceptions.auth import UserAlreadyExistsException, UserDoesNotExistsException
from app.exceptions.categories import CategoryDoesNotExistsException
from app.exceptions.products import ProductDoesNotExistsException
from app.exceptions.reviews import ReviewDoesNotExistsException
from app.models import Category, Product, Review, User
from app.schemas import CreateUser

from .db import session_dependency


class _CheckerExistsByID[T: Base]:
    def __init__(
        self,
        CrudManager: type[BaseCrudManager],
        exc_type: type[BaseApplicationException],
    ):
        self.CrudManager = CrudManager
        self.exc_type = exc_type

    async def __call__(self, session: session_dependency, id: UUID) -> T:
        value = await self.CrudManager.select_by_id(session, id)
        if value is None:
            raise self.exc_type(status_code=status.HTTP_404_NOT_FOUND)
        return value


_checker_category_exists = _CheckerExistsByID[Category](
    CategoryCrudManager, CategoryDoesNotExistsException
)
_checker_product_exists = _CheckerExistsByID[Product](
    ProductCrudManager, ProductDoesNotExistsException
)
_checker_user_exists = _CheckerExistsByID[User](
    UserCrudManager, UserDoesNotExistsException
)
_checker_review_exists = _CheckerExistsByID[Review](
    ReviewCrudManager, ReviewDoesNotExistsException
)


async def check_category_exists(
    session: session_dependency, category_id: UUID
) -> Category:
    return await _checker_category_exists(session, category_id)


async def check_product_exists(
    session: session_dependency, product_id: UUID
) -> Product:
    return await _checker_product_exists(session, product_id)


async def check_user_exists(session: session_dependency, user_id: UUID) -> User:
    return await _checker_user_exists(session, user_id)


async def check_review_exists(session: session_dependency, review_id: UUID) -> Review:
    return await _checker_review_exists(session, review_id)


async def check_user_by_username_or_email(
    session: session_dependency, user: CreateUser
) -> NoReturn | None:
    checked_user = await UserCrudManager.select_by_username_or_email(
        session, user.username, user.email
    )
    if checked_user is not None:
        raise UserAlreadyExistsException(status_code=status.HTTP_409_CONFLICT)
