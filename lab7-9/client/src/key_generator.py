import os


class AesGenerator:
    def __init__(self, key_bits: int = 256):
        if key_bits not in (128, 192, 256):
            raise ValueError("key_bits must be 128, 192, or 256")

        self.key_bits = key_bits

    def generate_secret_key(self) -> bytes:
        return os.urandom(self.key_bits // 8)
