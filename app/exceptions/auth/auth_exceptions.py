from dataclasses import dataclass
from typing import Literal

from .base import BaseJWTException, BaseUserException


@dataclass(kw_only=True)
class IncorrectUsernameOrPasswordException(BaseUserException):
    status_code: int = 401

    @property
    def message(self) -> str:
        return "Incorrect username or password"


@dataclass(kw_only=True)
class UserDoesNotExistsException(BaseUserException):
    status_code: int = 401

    @property
    def message(self) -> str:
        return "This user does not exists"


@dataclass(kw_only=True)
class SupplierDoesNotExistsException(BaseUserException):
    status_code: int = 403

    @property
    def message(self) -> str:
        return "This supplier does not exists"


@dataclass(kw_only=True)
class CustomerDoesNotExistsException(BaseUserException):
    status_code: int = 403

    @property
    def message(self) -> str:
        return "This customer does not exists"


@dataclass(kw_only=True)
class AdminDoesNotExistsException(BaseUserException):
    status_code: int = 403

    @property
    def message(self) -> str:
        return "This admin does not exists"


@dataclass(kw_only=True)
class UserAlreadyExistsException(BaseUserException):
    status_code: int = 409

    @property
    def message(self) -> str:
        return "This user already exists"


@dataclass(kw_only=True)
class InvalidJWTException(BaseJWTException):
    status_code: int = 401

    @property
    def message(self) -> str:
        return "Invalid token"


@dataclass(kw_only=True)
class InvalidJWTPayloadException(BaseJWTException):
    status_code: int = 401

    @property
    def message(self) -> str:
        return "Invalid token payload"


@dataclass(kw_only=True)
class InvalidJWTTypeException(BaseJWTException):
    status_code: int = 401
    type_: Literal["access", "refresh"] | None = None

    @property
    def message(self) -> str:
        if not self.type_:
            return f"Invalid token type. Must be one of {self.token_types!r}"
        return f"Invalid token type. Must be {self.type_!r}"


@dataclass(kw_only=True)
class ExpiredJWTException(BaseJWTException):
    status_code: int = 401

    @property
    def message(self) -> str:
        return "Token has expired"
