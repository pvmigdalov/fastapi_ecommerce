from dataclasses import dataclass
from typing import Literal

from .base import BaseJWTException, BaseUserException


@dataclass(kw_only=True)
class IncorrectUsernameOrPasswordException(BaseUserException):
    @property
    def message(self):
        return "Incorrect username or password"


@dataclass(kw_only=True)
class UserDoesNotExistsException(BaseUserException):
    @property
    def message(self):
        return "This user does not exist"


@dataclass(kw_only=True)
class SupplierDoesNotExistsException(BaseUserException):
    @property
    def message(self):
        return "This supplier does not exist"


@dataclass(kw_only=True)
class CustomerDoesNotExistsException(BaseUserException):
    @property
    def message(self):
        return "This customer does not exist"


@dataclass(kw_only=True)
class AdminDoesNotExistsException(BaseUserException):
    @property
    def message(self):
        return "This admin does not exist"


@dataclass(kw_only=True)
class InvalidJWTException(BaseJWTException):
    @property
    def message(self):
        return "Invalid token"


@dataclass(kw_only=True)
class InvalidJWTPayloadException(BaseJWTException):
    @property
    def message(self):
        return "Invalid token payload"


@dataclass(kw_only=True)
class InvalidJWTTypeException(BaseJWTException):
    type_: Literal["access", "refresh"] | None = None

    @property
    def message(self):
        if not self.type_:
            return f"Invalid token type. Must be one of {self.token_types!r}"
        return f"Invalid token type. Must be {self.type_!r}"


@dataclass(kw_only=True)
class ExpiredJWTException(BaseJWTException):
    @property
    def message(self):
        return "Token has expired"
