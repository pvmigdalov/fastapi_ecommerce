from dataclasses import dataclass

from .base import BaseCategoryException


@dataclass(kw_only=True)
class CategoryDoesNotExistsException(BaseCategoryException):
    status_code: int = 404

    @property
    def message(self) -> str:
        return "This category does not exists"


@dataclass(kw_only=True)
class CategoryAlreadyExistsException(BaseCategoryException):
    status_code: int = 409

    @property
    def message(self) -> str:
        return "This category already exists"
