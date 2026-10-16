from dataclasses import dataclass

from ..base import BaseApplicationException


@dataclass(kw_only=True)
class BaseCategoryException(BaseApplicationException):
    status_code: int = 500

    @property
    def message(self) -> str:
        return "An unknown categorie's error has occurred"
