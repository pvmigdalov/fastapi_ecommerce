from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.crud import UserCrudManager
from app.schemas import CreateUser
from app.dependencies import AuthHelper, check_user_by_username_or_email
from app.models import User


router = APIRouter(prefix="/auth", tags=["Auth"])
session_dependency = Annotated[AsyncSession, Depends(get_db_session)]

@router.post("/", status_code=status.HTTP_201_CREATED, dependencies=[Depends(check_user_by_username_or_email)])
async def create_user(session: session_dependency, user: CreateUser):
    user_data = user.model_dump()
    password = user_data.pop("password")
    user_data["hashed_password"] = AuthHelper.bcrypt_context.hash(password)

    await UserCrudManager.insert(session, **user_data)
    return {"transaction": "Successful"}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")

@router.post("/token")
async def get_token(
    session: session_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    user = await AuthHelper.authenticate_user(session, form_data.username, form_data.password)
    return {
        "access_token": user.username,
        "token_type": "bearer"
    }

@router.get("/me")
async def me(user: Annotated[str, Depends(oauth2_scheme)]):
    return user