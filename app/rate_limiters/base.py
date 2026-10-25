from abc import ABC, abstractmethod


class BaseRateLimiter(ABC):
    @abstractmethod
    async def __call__(self, key: str) -> tuple[bool, int]: ...
