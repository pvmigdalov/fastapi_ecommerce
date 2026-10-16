from datetime import datetime, timedelta, timezone
from typing import Literal
from uuid import UUID

import jwt
from fastapi import HTTPException, status
from pwdlib import PasswordHash
from pydantic import BaseModel, ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud import UserCrudManager
from app.exceptions.auth import (
    AdminDoesNotExistsException,
    CustomerDoesNotExistsException,
    ExpiredJWTException,
    IncorrectUsernameOrPasswordException,
    InvalidJWTException,
    InvalidJWTPayloadException,
    InvalidJWTTypeException,
    SupplierDoesNotExistsException,
    UserDoesNotExistsException,
)
from app.exceptions.auth.base import (
    BaseAuthException,
    BaseJWTException,
)
from app.models import User, UserRole
from app.settings import settings
from app.utils import non_instantiable


class JWTPayload(BaseModel):
    sub: str
    user_id: str
    user_role: str
    type: Literal["access", "refresh"]
    iat: int
    exp: int


@non_instantiable
class AuthHelper:
    password_util: PasswordHash = PasswordHash.recommended()
    jwt_algorithm: str = settings.auth_settings.jwt_algorithm
    jwt_secret_key: str = settings.auth_settings.jwt_secret_key.get_secret_value()
    jwt_expires_days: int = settings.auth_settings.jwt_expires_days
    jwt_refresh_expires_days: int = settings.auth_settings.jwt_refresh_expires_days

    @classmethod
    async def authenticate_user(
        cls,
        session: AsyncSession,
        username: str,
        password: str,
    ) -> User:
        user = await UserCrudManager.select_by_username(session, username)
        if (
            not user
            or not cls.password_util.verify(password, user.hashed_password)
            or not user.is_active
        ):
            raise IncorrectUsernameOrPasswordException(
                status_code=status.HTTP_401_UNAUTHORIZED
            )
        return user

    @classmethod
    async def get_current_user(
        cls,
        session: AsyncSession,
        user_jwt: str,
    ) -> User:
        payload = cls.verify_token(user_jwt, type_="access")
        user = await UserCrudManager.select_by_id(session, UUID(payload.user_id))
        if not user or not user.is_active:
            raise UserDoesNotExistsException(status_code=status.HTTP_401_UNAUTHORIZED)
        return user

    @classmethod
    async def get_current_supplier(cls, session: AsyncSession, user_jwt: str) -> User:
        user = await cls.get_current_user(session, user_jwt)
        if user.user_role == UserRole.CUSTOMER:
            raise SupplierDoesNotExistsException(status_code=status.HTTP_403_FORBIDDEN)
        return user

    @classmethod
    async def get_current_customer(cls, session: AsyncSession, user_jwt: str) -> User:
        user = await cls.get_current_user(session, user_jwt)
        if user.user_role == UserRole.SUPPLIER:
            raise CustomerDoesNotExistsException(status_code=status.HTTP_403_FORBIDDEN)
        return user

    @classmethod
    async def get_current_admin(cls, session: AsyncSession, user_jwt: str) -> User:
        user = await cls.get_current_user(session, user_jwt)
        if user.user_role != UserRole.ADMIN:
            raise AdminDoesNotExistsException(status_code=status.HTTP_403_FORBIDDEN)
        return user

    @classmethod
    def create_token(
        cls, user: User, type_: Literal["access", "refresh"] = "access"
    ) -> str:
        if type_ == "access":
            expires_days = cls.jwt_expires_days
        elif type_ == "refresh":
            expires_days = cls.jwt_refresh_expires_days
        else:
            raise InvalidJWTTypeException()

        # Validating jwt payload
        now = datetime.now(timezone.utc)
        payload = JWTPayload(
            sub=user.username,
            user_id=str(user.id),
            user_role=user.user_role.value,
            type=type_,
            iat=int(now.timestamp()),
            exp=int((now + timedelta(days=expires_days)).timestamp()),
        )

        return jwt.encode(
            payload.model_dump(),
            key=cls.jwt_secret_key,
            algorithm=cls.jwt_algorithm,
        )

    @classmethod
    def verify_token(
        cls, token: str, type_: Literal["access", "refresh"] = "access"
    ) -> JWTPayload:
        jwt_decoded = cls._decode_token(token)

        try:
            payload = JWTPayload.model_validate(jwt_decoded)
        except ValidationError:
            raise InvalidJWTPayloadException()

        if payload.type != type_:
            raise InvalidJWTTypeException(type_=type_)
        return payload

    @classmethod
    def get_credentials_exception(
        cls, *, status_code: int = 401, detail: str = ""
    ) -> HTTPException:
        return HTTPException(
            status_code=status_code,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

    @classmethod
    def _decode_token(cls, token: str) -> dict:
        try:
            jwt_decoded = jwt.decode(
                token,
                key=cls.jwt_secret_key,
                algorithms=[cls.jwt_algorithm],
            )
        except jwt.ExpiredSignatureError:
            raise ExpiredJWTException()
        except jwt.InvalidTokenError:
            raise InvalidJWTException()
        except jwt.PyJWTError:
            raise BaseJWTException()
        except Exception:
            raise BaseAuthException()
        else:
            return jwt_decoded
