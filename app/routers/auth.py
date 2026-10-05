from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.auth_utils import AuthHelper
from app.crud import UserCrudManager
from app.dependencies import (
    check_user_by_username_or_email,
    session_dependency,
    get_current_user,
)
from app.models import User as UserModel
from app.schemas import CreateUser, User


router = APIRouter(prefix="/auth", tags=["Auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/token")


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(check_user_by_username_or_email)],
    response_model=User,
)
async def create_user(session: session_dependency, user: CreateUser):
    user_data = user.model_dump()
    password = user_data.pop("password")
    user_data["hashed_password"] = AuthHelper.password_util.hash(password)

    new_user = UserModel(**user_data)
    await UserCrudManager.add(session, new_user)
    return new_user


@router.post("/token")
async def get_token(
    session: session_dependency,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    user = await AuthHelper.authenticate_user(
        session, form_data.username, form_data.password
    )
    token = AuthHelper.create_access_token(user, timedelta(days=1))
    return {"access_token": token, "token_type": "bearer"}


@router.get("/me", response_model=User)
async def get_me(user: Annotated[UserModel, Depends(get_current_user)]):
    return user
