import pytest
from src.services.aes import AesService


@pytest.fixture
def aes_service():
    return AesService()


def test_aes_encrypt_decrypt_roundtrip(aes_service):
    key = aes_service.generate_secret_key()
    iv = aes_service.generate_iv()
    message = "Pack my box with five dozen liquor jugs."

    cipher_b64 = aes_service.encrypt(key, iv, message)
    plain = aes_service.decrypt(key, cipher_b64)

    assert plain == message


def test_aes_decrypt_with_wrong_key_fails(aes_service):
    key1 = aes_service.generate_secret_key()
    iv1 = aes_service.generate_iv()

    wrong_key = aes_service.generate_secret_key()

    cipher_b64 = aes_service.encrypt(key1, iv1, "secret text")

    with pytest.raises(Exception):
        aes_service.decrypt(wrong_key, cipher_b64)
