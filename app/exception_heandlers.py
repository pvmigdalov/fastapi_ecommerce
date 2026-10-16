from fastapi import FastAPI, HTTPException
from fastapi.requests import Request

from app.auth_utils.exceptions import (
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
from app.auth_utils.exceptions.base import (
    BaseAuthException,
    BaseJWTException,
    BaseUserException,
)

SERVICE_EXCEPTIONS = (
    BaseAuthException,
    BaseJWTException,
    BaseUserException,
    IncorrectUsernameOrPasswordException,
    UserDoesNotExistsException,
    SupplierDoesNotExistsException,
    CustomerDoesNotExistsException,
    AdminDoesNotExistsException,
    InvalidJWTTypeException,
    InvalidJWTPayloadException,
    ExpiredJWTException,
    InvalidJWTException,
)


def make_handler():
    async def handler(request: Request, exc: BaseAuthException):
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.message,
            headers=exc.headers,
        )

    return handler


def register_exception_handlers(app: FastAPI):
    for exc_type in SERVICE_EXCEPTIONS:
        app.add_exception_handler(exc_type, make_handler())
