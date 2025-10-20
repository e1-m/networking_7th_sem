import base64

from fastapi import APIRouter, Depends, Response

from src.deps import get_key_pool
from src.key_pool import KeyPool
from src.schemas import PublicKeyResponse

router = APIRouter(
    prefix="/crypto-keys",
    tags=["crypto"],
)


@router.get("/public-key", response_model=PublicKeyResponse)
async def get_public_key(pool: KeyPool = Depends(get_key_pool)):
    pub = await pool.get_random_public_key()

    return PublicKeyResponse(
        key_id=pub.id,
        public_key=base64.b64encode(pub.key_pem).decode("ascii")
    )
