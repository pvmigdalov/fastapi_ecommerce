from datetime import datetime, timedelta, timezone
from functools import lru_cache
from uuid import UUID

import jwt
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import UserCrudManager
from app.models import User
from app.settings import settings
from app.utils import non_instantiable


@non_instantiable
class AuthHelper:
    password_util: PasswordHash = PasswordHash.recommended()
    jwt_algorithm: str = settings.auth_settings.jwt_algorithm
    jwt_secret_key: str = settings.auth_settings.jwt_secret_key.get_secret_value()

    @classmethod
    async def authenticate_user(
        cls,
        session: AsyncSession,
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
    async def get_current_user(
        cls,
        session: AsyncSession,
        user_jwt: str,
    ) -> User:
        try:
            payload = cls.decode_token(user_jwt)
        except jwt.ExpiredSignatureError:
            raise cls.get_credentals_exception(detail="Token has expired")
        except jwt.PyJWTError:
            raise cls.get_credentals_exception(detail="Could not validate credentials")

        user_id = payload.get("id")
        if not user_id:
            raise cls.get_credentals_exception(detail="Could not validate credentials")

        user = await UserCrudManager.select_by_id(session, UUID(user_id))
        if not user or not user.is_active:
            raise cls.get_credentals_exception(detail="Could not validate credentials")

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
            key=cls.jwt_secret_key,
            algorithm=cls.jwt_algorithm,
        )

    @classmethod
    def decode_token(cls, jwt_token: str):
        payload = jwt.decode(
            jwt_token,
            key=cls.jwt_secret_key,
            algorithms=[cls.jwt_algorithm],
        )
        return payload

    @classmethod
    @lru_cache(1)
    def get_credentals_exception(detail: str = "") -> HTTPException:
        return HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
