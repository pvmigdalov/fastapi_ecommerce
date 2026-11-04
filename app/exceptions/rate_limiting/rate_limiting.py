from dataclasses import dataclass

from .base import BaseRateLimitingException


@dataclass(kw_only=True)
class TooManyRequestsException(BaseRateLimitingException):
    status_code: int = 429

    @property
    def message(self) -> str:
        return "Too many requests"
