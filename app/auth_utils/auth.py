from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import UserCrudManager
from app.database import get_db_session
from app.models import User
from app.utils import non_instantiable
from app.settings import settings


auth_settings = settings.auth_settings


@non_instantiable
class AuthHelper:
    password_util = PasswordHash.recommended()

    @classmethod
    async def authenticate_user(
        cls,
        session: Annotated[AsyncSession, Depends(get_db_session)],
        username: str,
        password: str,
    ) -> User:
        user = await UserCrudManager.select_by_condition(session, username=username)
        if (
            not user
            or not cls.password_util.verify(password, user.hashed_password)
            or not user.is_active
        ):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return user

    @classmethod
    def create_access_token(cls, user: User, expires_delta: timedelta) -> str:
        payload = {
            "sub": user.username,
            "id": str(user.id),
            "user_role": user.user_role.value,
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + expires_delta,
        }

        payload["exp"] = int(payload["exp"].timestamp())
        return jwt.encode(
            payload,
            key=auth_settings.jwt_secret_key.get_secret_value(),
            algorithm=auth_settings.jwt_algorithm,
        )

    @classmethod
    def decode_token(cls, jwt_token: str):
        payload = jwt.decode(
            jwt_token,
            key=auth_settings.jwt_secret_key.get_secret_value(),
            algorithms=[auth_settings.jwt_algorithm],
        )
        return payload
