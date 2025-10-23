import base64
from dataclasses import dataclass
import time

import aiohttp

from src.key_generator import AesGenerator
from src.rsa_encryptor import RsaEncryptor


@dataclass
class Session:
    session_id: str
    aes_key: bytes
    expires_at: int


@dataclass
class _PublicKey:
    public_key_pem: bytes
    key_id: str


class SessionManager:
    def __init__(
            self,
            base_url: str,
            http_client: aiohttp.ClientSession,
            key_generator: AesGenerator,

    ):
        self.base_url = base_url
        self.key_generator = key_generator
        self.http_client = http_client

        self._session: Session | None = None

    async def _fetch_public_key(self) -> _PublicKey:
        async with self.http_client.get(f"{self.base_url}/crypto-keys/public-key") as resp:
            data = await resp.json()

            return _PublicKey(
                public_key_pem=data["public_key"].encode("ascii"),
                key_id=data["key_id"],
            )

    async def _initiate_new_session(self) -> Session:
        public_key = await self._fetch_public_key()

        aes_key = self.key_generator.generate_secret_key()
        aes_key_b64 = base64.b64encode(aes_key).decode("ascii")

        encryptor = RsaEncryptor(public_key.public_key_pem)
        encrypted_aes_key_b64 = encryptor.encrypt(aes_key_b64)

        async with self.http_client.post(
                f"{self.base_url}/sessions",
                json={"aes_key_b64_encrypted": encrypted_aes_key_b64},
                headers={"x-rsa-id": f"{public_key.key_id}"},
        ) as resp:
            session_data = await resp.json()
            return Session(
                session_id=session_data["session_id"],
                expires_at=session_data["expires_at"],
                aes_key=aes_key,
            )

    async def get_session(self) -> Session:
        valid_session_exists = (self._session is not None) and self._session.expires_at >= int(time.time()) - 3

        if valid_session_exists:
            return self._session

        self._session = await self._initiate_new_session()
        return self._session
