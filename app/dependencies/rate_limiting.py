from pathlib import Path
from typing import Annotated

from fastapi import Depends, status
from redis.asyncio import Redis

from app.database.redis import async_get_redis_rate_limiter, get_redis_rate_limiter
from app.models import User
from app.exceptions.rate_limiting import TooManyRequestsException
from app.rate_limiters import AntiSpamRateLimiter
from app.settings import settings

from .auth import get_current_user


lua_script_path = Path("app/rate_limiters/lua/anti_spam_interval.lua").absolute()
redis_rate_limiter_client = get_redis_rate_limiter(
    settings.redis_settings.redis_rate_limiter_url
)
anti_spam_rate_limiter = AntiSpamRateLimiter(
    redis_client=redis_rate_limiter_client,
    interval_sec=60,
    lua_script_path=lua_script_path,
)


async def get_redis_client() -> Redis:
    return await async_get_redis_rate_limiter(
        settings.redis_settings.redis_rate_limiter_url
    )


async def anti_spam_by_user_id(
    redis_client: Annotated[Redis, Depends(get_redis_client)],
    user: Annotated[User, Depends(get_current_user)],
) -> None:
    key = f"anti-spam:{user.id}"
    allowed, wait_time = await anti_spam_rate_limiter(key)
    if not allowed:
        raise TooManyRequestsException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many requests. Try in {wait_time} sec.",
        )
