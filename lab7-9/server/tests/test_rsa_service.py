import pytest
from src.services.rsa import RsaService


@pytest.fixture
def rsa_service():
    return RsaService()


def test_rsa_encrypt_decrypt_roundtrip(rsa_service):
    keys = rsa_service.generate_crypto_keys()
    message = "Sphinx of black quartz, judge my vow."

    cipher_b64 = rsa_service.encrypt(keys.public_key_pem, message)
    plain = rsa_service.decrypt(keys.private_key_pem, cipher_b64)

    assert plain == message


def test_rsa_decrypt_with_wrong_key_fails(rsa_service):
    keys = rsa_service.generate_crypto_keys()
    wrong_keys = rsa_service.generate_crypto_keys()

    cipher_b64 = rsa_service.encrypt(keys.public_key_pem, "hello")
    with pytest.raises(Exception):
        _ = rsa_service.decrypt(wrong_keys.private_key_pem, cipher_b64)
