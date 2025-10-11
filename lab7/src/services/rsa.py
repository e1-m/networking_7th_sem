import base64
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from dataclasses import dataclass


@dataclass
class RsaKeysData:
    public_key_pem: bytes
    private_key_pem: bytes


class RsaService:
    def generate_crypto_keys(self, key_size: int = 2048) -> RsaKeysData:
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        public_pem = private_key.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo,
        )
        return RsaKeysData(public_key_pem=public_pem, private_key_pem=private_pem)

    def encrypt(self, public_key_pem: bytes, plain_text: str) -> str:
        public_key = serialization.load_pem_public_key(public_key_pem)
        cipher_bytes = public_key.encrypt(
            plain_text.encode('utf-8'),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )
        return base64.b64encode(cipher_bytes).decode('ascii')

    def decrypt(self, private_key_pem: bytes, cipher_text_b64: str) -> str:
        private_key = serialization.load_pem_private_key(private_key_pem, password=None)
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
