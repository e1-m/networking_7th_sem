import base64
from abc import ABC, abstractmethod

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


class Decryptor(ABC):
    @abstractmethod
    def decrypt(self, cipher_text_b64): ...


class RsaDecryptor(Decryptor):
    def __init__(self, private_key_pem: bytes) -> None:
        self.private_key_pem = private_key_pem

    def decrypt(self, cipher_text_b64: str) -> str:
        private_key = serialization.load_pem_private_key(self.private_key_pem, password=None)
        cipher_bytes = base64.b64decode(cipher_text_b64)
        plain_bytes = private_key.decrypt(
            cipher_bytes,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return plain_bytes.decode('utf-8')
