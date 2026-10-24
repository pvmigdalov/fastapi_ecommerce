from typing import Annotated, NoReturn

from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer

from app.auth_utils import AuthHelper
from app.crud import (
    UserCrudManager,
)
from app.models import Product, User, Review
from app.schemas import CreateUser
from app.exceptions.auth import (
    CustomerDoesNotExistsException,
    UserAlreadyExistsException,
    SupplierDoesNotExistsException,
)

from .db import session_dependency
from .existence_checks import check_product_exists, check_review_exists


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def check_user_by_username_or_email(
    session: session_dependency, user: CreateUser
) -> NoReturn | None:
    checked_user = await UserCrudManager.select_by_username_or_email(
        session, user.username, user.email
    )
    if checked_user is not None:
        raise UserAlreadyExistsException(status_code=status.HTTP_409_CONFLICT)


async def get_current_user(
    session: session_dependency, user_jwt: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    return await AuthHelper.get_current_user(session, user_jwt)


async def get_current_supplier(
    session: session_dependency, user_jwt: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    return await AuthHelper.get_current_supplier(session, user_jwt)


async def get_current_customer(
    session: session_dependency, user_jwt: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    return await AuthHelper.get_current_customer(session, user_jwt)


async def get_current_admin(
    session: session_dependency, user_jwt: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    return await AuthHelper.get_current_admin(session, user_jwt)


async def get_owned_product(
    user: Annotated[User, Depends(get_current_supplier)],
    product: Annotated[Product, Depends(check_product_exists)],
) -> Product:
    if product.supplier_id != user.id:
        raise SupplierDoesNotExistsException(status_code=status.HTTP_403_FORBIDDEN)
    return product


async def get_owned_review(
    user: Annotated[User, Depends(get_current_customer)],
    review: Annotated[Review, check_review_exists],
) -> Review:
    if review.user_id != user.id:
        raise CustomerDoesNotExistsException(status_code=status.HTTP_403_FORBIDDEN)
    return review
