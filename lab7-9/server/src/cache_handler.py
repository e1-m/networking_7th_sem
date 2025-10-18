import json
from abc import ABC, abstractmethod

from redis.asyncio import Redis

CacheValue = dict | list | str


class CacheHandler(ABC):
    @abstractmethod
    async def get(self, key: str) -> CacheValue | None:
        ...

    @abstractmethod
    async def set(self, key: str, value: CacheValue, **kwargs) -> None:
        ...

    @abstractmethod
    async def delete(self, key: str) -> None:
        ...


class InMemoryCacheHandler(CacheHandler):
    def __init__(self):
        self.cache = {}

    async def get(self, key: str) -> CacheValue | None:
        return self.cache.get(key)

    async def set(self, key: str, value: CacheValue, **kwargs) -> None:
        self.cache[key] = value

    async def delete(self, key: str) -> None:
        if key in self.cache:
            del self.cache[key]


class RedisCacheHandler(CacheHandler):
    def __init__(self, redis: Redis):
        self.redis = redis

    async def get(self, key: str) -> CacheValue | None:
        if (result := await self.redis.get(key)) is None:
            return None

        if isinstance(result, bytes):
            result = result.decode("utf-8")

        try:
            value = json.loads(result)
        except json.decoder.JSONDecodeError:
            value = result

        return value

    async def set(self, key: str, value: CacheValue, **kwargs) -> None:
        await self.redis.set(key, json.dumps(value), **kwargs)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)
