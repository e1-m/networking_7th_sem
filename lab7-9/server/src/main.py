from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.deps import get_redis, get_cache_handler
from src.errors import (
    CryptographyServiceError,
    ResourceNotFound,
    CorruptedRequest,
    MissingHeader,
    InvalidSession
)
from src.routers import crypto, echo, sessions

api = APIRouter(prefix="/api")

api.include_router(crypto.router)
api.include_router(sessions.router)
api.include_router(echo.router)


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = get_redis()
    await redis.ping()
    app.state.cache_handler = get_cache_handler(redis)
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(api)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_exception_handler(status_code, initial_detail):
    async def exception_handler(_: Request, exc: CryptographyServiceError) -> JSONResponse:
        content = {"detail": exc.message if exc.message else initial_detail}
        return JSONResponse(status_code=status_code, content=content, headers=exc.headers)

    return exception_handler


exception_handlers = [
    (CryptographyServiceError, status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error"),
    (ResourceNotFound, status.HTTP_404_NOT_FOUND, "Resource not found"),
    (CorruptedRequest, status.HTTP_400_BAD_REQUEST, "Corrupted Request"),
    (MissingHeader, status.HTTP_401_UNAUTHORIZED, "Missing Header"),
    (InvalidSession, status.HTTP_401_UNAUTHORIZED, "Invalid Session"),
]

for exc_class, status_code, message in exception_handlers:
    app.add_exception_handler(
        exc_class_or_status_code=exc_class,
        handler=create_exception_handler(status_code, message)
    )
