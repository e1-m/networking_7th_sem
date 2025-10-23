import uuid
import time

from fastapi import APIRouter, Depends

from src.cache_handler import CacheHandler
from src.config import settings
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
    expires_at = int(time.time()) + settings.SESSION_EXPIRATION_SECONDS
    session_id = str(uuid.uuid4())

    session = Session(
        session_id=session_id,
        aes_key_b64=aes_key_b64,
        expires_at=expires_at,
    )

    await cache.set(
        f"session:{session_id}",
        session.model_dump(mode="json"),
        ex=settings.SESSION_EXPIRATION_SECONDS
    )

    return session
