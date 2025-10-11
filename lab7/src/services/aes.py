import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class AesService:
    def generate_secret_key(self, key_bits: int = 256) -> bytes:
        if key_bits not in (128, 192, 256):
            raise ValueError("key_bits must be 128, 192, or 256")

        key = os.urandom(key_bits // 8)

        return key

    def generate_iv(self) -> bytes:
        return os.urandom(12)

    def encrypt(self, key: bytes, iv: bytes, plain_text: str) -> str:
        aesgcm = AESGCM(key)
        ct = aesgcm.encrypt(iv, plain_text.encode('utf-8'), associated_data=None)
        packed = iv + ct
        return base64.b64encode(packed).decode('ascii')

    def decrypt(self, key: bytes, cipher_text_b64: str) -> str:
        packed = base64.b64decode(cipher_text_b64)
        iv = packed[:12]
        ct = packed[12:]
        aesgcm = AESGCM(key)
        pt = aesgcm.decrypt(iv, ct, associated_data=None)
        return pt.decode('utf-8')
