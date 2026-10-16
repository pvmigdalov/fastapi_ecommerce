from dataclasses import dataclass, field
from typing import ClassVar

from ..base import BaseApplicationException


@dataclass(kw_only=True)
class BaseAuthException(BaseApplicationException):
    status_code: int = 500
    headers: dict[str, str] = field(
        default_factory=lambda: {"WWW-Authenticate": "Bearer"}
    )

    @property
    def message(self) -> str:
        return "An unknown authenticate error has occurred"


@dataclass(kw_only=True)
class BaseUserException(BaseAuthException):
    status_code: int = 500

    @property
    def message(self) -> str:
        return "An unknown user authenticate error has occurred"


@dataclass(kw_only=True)
class BaseJWTException(BaseAuthException):
    token_types: ClassVar[tuple[str, ...]] = (
        "access",
        "refresh",
    )

    status_code: int = 401

    @property
    def message(self) -> str:
        return "An uknown JWT decoding error has occurred"
