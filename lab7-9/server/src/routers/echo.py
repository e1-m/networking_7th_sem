import base64
from datetime import datetime

import time

from fastapi import APIRouter, Request
from fastapi.routing import APIRoute

from src.aes import AesCryptor
from src.errors import MissingSessionHeader, InvalidSession
from src.schemas import IdResponse, MessageIn, MessageOut, Session


class EncryptedRoute(APIRoute):
    def get_route_handler(self):
        original = super().get_route_handler()

        async def custom_route_handler(request: Request):
            if not (session_id := request.headers.get("session-id")):
                raise MissingSessionHeader("Missing session-id header")

            cache = request.app.state.cache_handler

            if (session_data := await cache.get(f"session:{session_id}")) is None:
                raise InvalidSession("Invalid or expired session")

            session = Session(**session_data)
            cryptor = AesCryptor(base64.b64decode(session.aes_key_b64))

            if body := await request.body():
                request._body = cryptor.decrypt(base64.b64encode(body).decode('ascii'))

            response = await original(request)

            if hasattr(response, "body"):
                body_bytes = response.body
                response.body = cryptor.encrypt(body_bytes)
                response.headers["content-length"] = str(len(response.body))

            return response

        return custom_route_handler


router = APIRouter(
    prefix="/echo",
    tags=["echo"],
    route_class=EncryptedRoute
)


@router.post("/", response_model=IdResponse)
def echo(
        message: MessageIn,
):
    return MessageOut(message=f"[{datetime.fromtimestamp(time.time())}] {message.message}")
