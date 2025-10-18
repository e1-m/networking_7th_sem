from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status, APIRouter
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.errors import (
    CryptographyServiceError,
    ResourceNotFound
)
from src.routers import crypto

api = APIRouter(prefix="/api")

api.include_router(crypto.router)


@asynccontextmanager
async def lifespan(app: FastAPI):
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
]

for exc_class, status_code, message in exception_handlers:
    app.add_exception_handler(
        exc_class_or_status_code=exc_class,
        handler=create_exception_handler(status_code, message)
    )
