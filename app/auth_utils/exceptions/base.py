from dataclasses import dataclass, field
from typing import ClassVar


@dataclass(kw_only=True)
class BaseAuthException(Exception):
    status_code: int = 500
    headers: dict[str, str] = field(
        default_factory=lambda: {"WWW-Authenticate": "Bearer"}
    )

    @property
    def message(self):
        return "An unknown error has occurred"


@dataclass(kw_only=True)
class BaseUserException(BaseAuthException):
    @property
    def message(self):
        return "An unknown user authenticate error has occurred"


@dataclass(kw_only=True)
class BaseJWTException(BaseAuthException):
    token_types: ClassVar[tuple[str, ...]] = (
        "access",
        "refresh",
    )

    status_code: int = 401

    @property
    def message(self):
        return "An uknown JWT decoding error has occurred"
