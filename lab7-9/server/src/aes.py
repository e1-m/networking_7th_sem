import base64
import os

from cryptography.hazmat.primitives.ciphers.aead import AESGCM


class AesCryptor:
    def __init__(self, key: bytes, iv_bits: int = 12):
        self.aesgcm = AESGCM(key)
        self.iv_bits = iv_bits

    def encrypt(self, plain: bytes) -> bytes:
        iv = os.urandom(self.iv_bits)
        ct = self.aesgcm.encrypt(iv, plain, associated_data=None)
        return base64.b64encode(iv + ct)

    def decrypt(self, cipher_b64: str | bytes) -> bytes:
        packed = base64.b64decode(cipher_b64)
        iv, ct = packed[:12], packed[12:]
        return self.aesgcm.decrypt(iv, ct, associated_data=None)
