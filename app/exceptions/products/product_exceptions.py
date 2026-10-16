from dataclasses import dataclass

from .base import BaseProductException


@dataclass(kw_only=True)
class ProductDoesNotExistsException(BaseProductException):
    status_code: int = 404

    @property
    def message(self) -> str:
        return "This product does not exists"


@dataclass(kw_only=True)
class ProductAlreadyExistsException(BaseProductException):
    status_code: int = 409

    @property
    def message(self) -> str:
        return "This product already exists"
