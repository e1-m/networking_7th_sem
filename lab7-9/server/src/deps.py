from functools import lru_cache
from typing import Annotated

from fastapi import Depends
from redis.asyncio import Redis

from src.cache_handler import CacheHandler, RedisCacheHandler
from src.config import settings
from src.key_generator import KeyPairGenerator, RsaKeyPairGenerator
from src.key_pool import KeyPool
from src.services.rsa import RsaService


def get_rsa_service() -> RsaService:
    return RsaService(

    )


@lru_cache
def get_redis() -> Redis:
    return Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT
    )


RedisDep = Annotated[Redis, Depends(get_redis)]


@lru_cache
def get_cache_handler(redis: RedisDep) -> CacheHandler:
    return RedisCacheHandler(
        redis=redis,
    )


CacheHandlerDep = Annotated[CacheHandler, Depends(get_cache_handler)]


@lru_cache
def get_keypair_generator() -> KeyPairGenerator:
    return RsaKeyPairGenerator()


KeyPairGeneratorDep = Annotated[KeyPairGenerator, Depends(get_keypair_generator)]


@lru_cache
def get_key_pool(cache_handler: CacheHandlerDep, keypair_generator: KeyPairGeneratorDep) -> KeyPool:
    return KeyPool(
        cache_handler=cache_handler,
        keypair_generator=keypair_generator,
        size=settings.KEY_POOL_SIZE,
    )
