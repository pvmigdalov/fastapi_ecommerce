from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass(kw_only=True)
class BaseApplicationException(Exception, ABC):
    status_code: int = 500
    headers: dict[str, str] = field(default_factory=dict)

    @property
    @abstractmethod
    def message(self) -> str:
        return "An unknown application error has occurred"
