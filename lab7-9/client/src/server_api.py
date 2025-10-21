import json

import aiohttp
from pydantic import BaseModel

from src.aes_cryptor import AesCryptor
from src.session_manager import SessionManager


class MessageIn(BaseModel):
    message: str


class MessageOut(BaseModel):
    message: str


class ServerApi:
    def __init__(self, base_url: str, http_client: aiohttp.ClientSession, session_manager: SessionManager):
        self.base_url = base_url
        self.http_client = http_client
        self.session_manager = session_manager

    async def echo(self, message: MessageIn) -> MessageOut:
        session = await self.session_manager.get_session()
        cryptor = AesCryptor(session.aes_key)

        plaintext_bytes = json.dumps(message.model_dump(mode="json")).encode("utf-8")
        encrypted_body_b64 = cryptor.encrypt(plaintext_bytes)

        async with self.http_client.post(
                f"{self.base_url}/echo/",
                data=encrypted_body_b64,
                headers={"session-id": session.session_id, "content-type": "application/json"},
        ) as resp:
            enc_response = await resp.read()
            decrypted = cryptor.decrypt(enc_response.decode("utf-8"))
            return MessageOut(**json.loads(decrypted.decode("utf-8")))
