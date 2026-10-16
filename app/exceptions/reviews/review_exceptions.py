from dataclasses import dataclass

from .base import BaseReviewException


@dataclass(kw_only=True)
class ReviewDoesNotExistsException(BaseReviewException):
    status_code: int = 404

    @property
    def message(self) -> str:
        return "This review does not exists"


@dataclass(kw_only=True)
class ReviewAlreadyExistsException(BaseReviewException):
    status_code: int = 409

    @property
    def message(self) -> str:
        return "This review already exists"
