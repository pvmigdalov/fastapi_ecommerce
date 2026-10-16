from dataclasses import dataclass

from ..base import BaseApplicationException


@dataclass(kw_only=True)
class BaseProductException(BaseApplicationException):
    status_code: int = 500

    @property
    def message(self) -> str:
        return "An unknown product's error has occurred"
