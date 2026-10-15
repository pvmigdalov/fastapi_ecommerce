from typing import Literal
from .base import BaseJWTException, BaseUserException


class IncorrectUsernameOrPasswordException(BaseUserException):
    @property
    def message(self):
        return "Incorrect username or password"


class UserDoesNotExistsException(BaseUserException):
    @property
    def message(self):
        return "User doesn't exists"


class SupplierDoesNotExistsException(BaseUserException):
    @property
    def message(self):
        return "Supplier doesn't exists"


class CustomerDoesNotExistsException(BaseUserException):
    @property
    def message(self):
        return "Customer doesn't exists"


class AdminDoesNotExistsException(BaseUserException):
    @property
    def message(self):
        return "Admin doesn't exists"


class InvalidJWTException(BaseJWTException):
    @property
    def message(self):
        return "Invalid token"


class InvalidJWTPayloadException(BaseJWTException):
    @property
    def message(self):
        return "Invalid token payload"


class InvalidJWTTypeException(BaseJWTException):
    def __init__(self, type_: Literal["access", "refresh"] | None = None):
        self.type_ = type_

    @property
    def message(self):
        if not self.type_:
            return f"Invalid token type. Must be one of {self.token_types!r}"
        return f"Invalid token type. Must be {self.type_!r}"


class ExpiredJWTException(BaseJWTException):
    @property
    def message(self):
        return "Token has expired"
