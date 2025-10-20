from functools import lru_cache
from typing import Annotated

from fastapi import Depends, Header
from redis.asyncio import Redis

from src.cache_handler import CacheHandler, RedisCacheHandler
from src.config import settings
from src.decryptor import RsaDecryptor, Decryptor
from src.key_generator import KeyPairGenerator, RsaKeyPairGenerator
from src.key_pool import KeyPool


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


async def get_decryptor(key_id: str = Header(alias="x-rsa-id"),
                        key_pool: KeyPool = Depends(get_key_pool)) -> Decryptor:
    return RsaDecryptor(
        private_key_pem=await key_pool.get_private_key(key_id),
    )
