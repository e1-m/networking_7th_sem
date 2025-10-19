import uuid

from fastapi import APIRouter, Depends

from src.cache_handler import CacheHandler
from src.decryptor import Decryptor
from src.deps import get_decryptor, get_cache_handler
from src.schemas import SessionOut, SessionIn, Session

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"],
)


@router.post("/", response_model=SessionOut)
async def create_session(
        session: SessionIn,
        cache: CacheHandler = Depends(get_cache_handler),
        decryptor: Decryptor = Depends(get_decryptor),
):
    # We should probably check if the received key is indeed a valid aes, but I'll skip it xD
    aes_key_b64 = decryptor.decrypt(session.aes_key_b64_encrypted)
    session_id = str(uuid.uuid4())

    await cache.set(f"session:{session_id}", Session(
        session_id=session_id,
        aes_key_b64=aes_key_b64,
    ).model_dump(mode="json"))

    return SessionOut(
        session_id=session_id,
    )
