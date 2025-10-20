import random
from dataclasses import dataclass

from src.cache_handler import CacheHandler
from src.errors import ResourceNotFound
from src.key_generator import KeyPairGenerator


@dataclass
class PublicKey:
    id: str
    key_pem: bytes


class KeyPool:
    def __init__(self, cache_handler: CacheHandler, keypair_generator: KeyPairGenerator, size: int):
        self.cache = cache_handler
        self.generator = keypair_generator
        self.size = size

    async def get_random_public_key(self) -> PublicKey:
        key_id = str(random.randint(0, self.size - 1))
        public_key = await self.cache.get(f"public-key-{key_id}")

        if not public_key:
            keypair = self.generator.generate_keypair()

            await self.cache.set(f"private-key-{key_id}", keypair.private_key_pem.decode("ascii"))
            await self.cache.set(f"public-key-{key_id}", keypair.public_key_pem.decode("ascii"))

            return PublicKey(id=key_id, key_pem=keypair.public_key_pem)

        return PublicKey(id=key_id, key_pem=public_key.encode("ascii"))

    async def get_private_key(self, key_id) -> bytes:
        key = await self.cache.get(f"private-key-{key_id}")

        if not key_id:
            raise ResourceNotFound("Public key not found")

        return key.encode("ascii")
