import base64

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding


class RsaEncryptor:
    def __init__(self, public_key_pem: bytes) -> None:
        self.public_key_pem = public_key_pem

    def encrypt(self, plain_text: str) -> str:
        public_key = serialization.load_pem_public_key(self.public_key_pem)
        cipher_bytes = public_key.encrypt(
            plain_text.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return base64.b64encode(cipher_bytes).decode('ascii')
