from asyncio import Lock
from pathlib import Path

from redis.asyncio import Redis

from .base import BaseRateLimiter


class AntiSpamRateLimiter(BaseRateLimiter):
    def __init__(self, redis_client: Redis, interval_sec: float, lua_script_path: Path):
        self.redis_client = redis_client
        self.interval_sec = interval_sec
        self.lua_script_path = lua_script_path
        self.script_sha = None
        self._lock = Lock()

    async def __call__(self, key: str) -> tuple[bool, int]:
        if self.script_sha is None:
            await self._load_script()

        # fail script load
        if self.script_sha is None:
            return True, 0

        try:
            res = await self.redis_client.evalsha(
                self.script_sha,
                1,
                key,
                self.interval_sec,
            )
        except Exception:
            return True, 0

        allowed = bool(res[0])
        wait_time = int(res[1]) if len(res) > 1 else 0
        return allowed, wait_time

    async def _load_script(self) -> None:
        async with self._lock:
            if self.script_sha is None:
                script = self.lua_script_path.read_text(encoding="utf-8")
                self.script_sha = await self.redis_client.script_load(script)

    # @classmethod
    # async def create(
    #     cls, redis_client: Redis, interval_sec: float, lua_script_path: Path
    # ) -> Self:
    #     self = super().__new__(cls)
    #     self.redis_client = redis_client  # ty: ignore [unresolved-attribute]
    #     self.interval_sec = interval_sec  # ty: ignore [unresolved-attribute]
    #     self.script_sha = await cls._load_script(self.redis_client, lua_script_path)  # ty: ignore [unresolved-attribute]
    #     return self
