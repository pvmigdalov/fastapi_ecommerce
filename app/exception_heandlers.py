import itertools

from fastapi import FastAPI, HTTPException
from fastapi.requests import Request

from app.exceptions import BaseApplicationException
from app.exceptions import auth as auth_exc
from app.exceptions import categories as categories_exc
from app.exceptions import products as products_exc
from app.exceptions import reviews as reviews_exc


AUTH_EXCEPTIONS = (
    auth_exc.base.BaseAuthException,
    auth_exc.base.BaseJWTException,
    auth_exc.base.BaseUserException,
    auth_exc.IncorrectUsernameOrPasswordException,
    auth_exc.UserDoesNotExistsException,
    auth_exc.SupplierDoesNotExistsException,
    auth_exc.CustomerDoesNotExistsException,
    auth_exc.AdminDoesNotExistsException,
    auth_exc.InvalidJWTTypeException,
    auth_exc.InvalidJWTPayloadException,
    auth_exc.ExpiredJWTException,
    auth_exc.InvalidJWTException,
)

CATEGORIES_EXCEPTIONS = (
    categories_exc.base.BaseCategoryException,
    categories_exc.CategoryAlreadyExistsException,
    categories_exc.CategoryDoesNotExistsException,
)

PRODUCTS_EXCEPTIONS = (
    products_exc.base.BaseProductException,
    products_exc.ProductAlreadyExistsException,
    products_exc.ProductDoesNotExistsException,
    products_exc.ProductsByCategoryNotFoundException,
)

REVIEWS_EXCEPTIONS = (
    reviews_exc.base.BaseReviewException,
    reviews_exc.ReviewAlreadyExistsException,
    reviews_exc.ReviewDoesNotExistsException,
)


def make_handler():
    async def handler(request: Request, exc: BaseApplicationException):
        raise HTTPException(
            status_code=exc.status_code,
            detail=exc.message,
            headers=exc.headers,
        )

    return handler


def register_exception_handlers(app: FastAPI):
    for exc_type in itertools.chain(
        AUTH_EXCEPTIONS, CATEGORIES_EXCEPTIONS, PRODUCTS_EXCEPTIONS, REVIEWS_EXCEPTIONS
    ):
        app.add_exception_handler(exc_type, make_handler())
