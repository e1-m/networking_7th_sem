from functools import lru_cache

from src.services.rsa import RsaService
from src.storage import InMemoryKeyStorage, Storage


def get_rsa_service() -> RsaService:
    return RsaService(

    )


@lru_cache
def get_storage() -> Storage:
    return InMemoryKeyStorage()
