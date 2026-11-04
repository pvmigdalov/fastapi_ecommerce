from dataclasses import dataclass

from .base import BaseRateLimitingException


@dataclass(kw_only=True)
class TooManyRequestsException(BaseRateLimitingException):
    status_code: int = 429
    detail: str

    @property
    def message(self) -> str:
        return self.detail
