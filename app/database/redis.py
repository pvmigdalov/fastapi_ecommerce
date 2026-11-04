from functools import lru_cache

from redis.asyncio import Redis


@lru_cache(1)
def get_redis_cache(url: str) -> Redis:
    return Redis.from_url(url, decode_responses=True)


@lru_cache(1)
def get_redis_rate_limiter(url: str) -> Redis:
    return Redis.from_url(url, decode_responses=True)


async def async_get_redis_cache(url: str) -> Redis:
    return get_redis_cache(url)


async def async_get_redis_rate_limiter(url: str) -> Redis:
    return get_redis_rate_limiter(url)
