from typing import Annotated

from fastapi import Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.database import get_db_session
from app.crud import UserCrudManager


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
    ):
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