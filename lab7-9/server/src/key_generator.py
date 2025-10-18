from abc import ABC, abstractmethod
from dataclasses import dataclass

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa


@dataclass
class KeyPair:
    public_key_pem: bytes
    private_key_pem: bytes


class KeyPairGenerator(ABC):
    @abstractmethod
    def generate_keypair(self) -> KeyPair: ...


class RsaKeyPairGenerator(KeyPairGenerator):
    def __init__(self, key_size=2048, public_exponent=65537):
        self.key_size = key_size
        self.public_exponent = public_exponent

    def generate_keypair(self) -> KeyPair:
        private_key = rsa.generate_private_key(public_exponent=self.public_exponent, key_size=self.key_size)
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return KeyPair(public_key_pem=public_pem, private_key_pem=private_pem)
