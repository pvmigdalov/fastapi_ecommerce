from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from passlib.context import CryptContext

from app.database import get_db_session
from app.crud import UserCrudManager
from app.schemas import CreateUser
from app.dependencies import check_user_by_username_or_email


router = APIRouter(prefix="/auth", tags=["Auth"])
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
session_dependency = Annotated[AsyncSession, Depends(get_db_session)]

@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_user_by_username_or_email)])
async def create_user(session: session_dependency, user: CreateUser):
    user_data = user.model_dump()
    password = user_data.pop("password")
    user_data["hashed_password"] = bcrypt_context.hash(password)

    await UserCrudManager.insert(session, **user_data)
    return {"transaction": "Successful"}

