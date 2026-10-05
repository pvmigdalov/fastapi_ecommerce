from typing import Annotated, NoReturn
from uuid import UUID

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.auth_utils import AuthHelper
from app.crud import (
    UserCrudManager,
)
from app.models import Product, User
from app.schemas import CreateUser

from .db import session_dependency
from .existence_checks import check_product_exists


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


async def check_user_by_username_or_email(
    session: session_dependency, user: CreateUser
) -> NoReturn | None:
    checked_user = await UserCrudManager.select_by_username_or_email(
        session, user.username, user.email
    )
    if checked_user is not None:
        raise HTTPException(
            status.HTTP_409_CONFLICT, "User with this username or email already exists"
        )


async def get_current_user(
    session: session_dependency, user_jwt: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    return await AuthHelper.get_current_user(session, user_jwt)


async def get_current_supplier(
    session: session_dependency, user_jwt: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    return await AuthHelper.get_current_supplier(session, user_jwt)


async def get_current_admin(
    session: session_dependency, user_jwt: Annotated[str, Depends(oauth2_scheme)]
) -> User:
    return await AuthHelper.get_current_admin(session, user_jwt)


async def get_owned_product(
    session: session_dependency,
    user_jwt: Annotated[str, Depends(oauth2_scheme)],
    product_id: UUID,
) -> Product:
    user = await AuthHelper.get_current_supplier(session, user_jwt)
    product = await check_product_exists(session, product_id)
    if user.id != product.supplier_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Forbidden")

    return product
