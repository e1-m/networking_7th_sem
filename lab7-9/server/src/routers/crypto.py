import base64

from fastapi import APIRouter, Depends

from src.deps import get_storage, get_rsa_service
from src.errors import ResourceNotFound
from src.schemas import IdResponse, PublicKeyResponse
from src.services.rsa import RsaService
from src.storage import Storage

router = APIRouter(
    prefix="/crypto-keys",
)


@router.post("/generate/rsa-keys", response_model=IdResponse)
def generate_rsa_keys(
        rsa_service: RsaService = Depends(get_rsa_service),
        storage: Storage = Depends(get_storage)
):
    keys = rsa_service.generate_crypto_keys()
    pub_b64 = base64.b64encode(keys.public_key_pem).decode("ascii")
    priv_b64 = base64.b64encode(keys.private_key_pem).decode("ascii")
    key_id = storage.add(pub_b64, priv_b64)
    return IdResponse(id=key_id)


@router.get("/rsa-public-key/{key_id}", response_model=PublicKeyResponse)
def get_public_key(key_id: int, storage: Storage = Depends(get_storage)):
    if not (pub := storage.get_public(key_id)):
        raise ResourceNotFound("RSA public key not found")

    return PublicKeyResponse(public_key=pub)
