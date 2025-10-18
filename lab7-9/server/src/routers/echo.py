from datetime import datetime

import time

from fastapi import APIRouter

from src.schemas import IdResponse, MessageIn, MessageOut

router = APIRouter(
    prefix="/echo",
    tags=["echo"]
)


@router.post("/", response_model=IdResponse)
def echo(
        message: MessageIn,
):
    return MessageOut(message=f"[{datetime.fromtimestamp(time.time())}] {message.message}")
