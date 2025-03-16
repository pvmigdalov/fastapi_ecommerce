import os
from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from dotenv import load_dotenv
from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.database import get_db_session
from app.crud import UserCrudManager
from app.models import User


load_dotenv("app/settings/auth.env")

ALGORITHM = os.getenv("JWT_ALGORITHM")
SECRET_KEY = os.getenv("JWT_SECRET_KEY")


class AuthHelper:

    bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def __new__(cls, *args, **kwargs):
        raise ValueError("This class does not involve creating instances.")

    @classmethod
    async def authenticate_user(
        cls,
        session: Annotated[AsyncSession, Depends(get_db_session)],
        username: str,
        password: str
    ) -> User:
        user = await UserCrudManager.select_by_condition(session, username=username)
        if not user \
            or not cls.bcrypt_context.verify(password, user.hashed_password) \
            or not user.is_active:
            
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return user
    
    @classmethod
    def create_access_token(
        cls,
        user: User,
        expires_delta: timedelta
    ) -> str:
        payload = {
            "sub": user.username,
            "id": user.id,
            "is_admin": user.is_admin,
            "is_supplier": user.is_supplier,
            "is_customer": user.is_customer,
            "exp": datetime.now(timezone.utc) + expires_delta
        }

        payload["exp"] = int(payload["exp"].timestamp())
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    @classmethod
    def decode_token(cls, jwt_token: str):
        payload = jwt.decode(jwt_token, key=SECRET_KEY, algorithms=[ALGORITHM])
        return payload