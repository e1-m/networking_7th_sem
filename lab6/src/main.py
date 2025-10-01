from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.errors import (
    EmployeeServiceError,
    EmployeeNotFoundError,
    EmployeeAlreadyExistsError
)
from src.routers import employee


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(employee.router)


def create_exception_handler(status_code, initial_detail):
    async def exception_handler(_: Request, exc: EmployeeServiceError) -> JSONResponse:
        content = {"detail": exc.message if exc.message else initial_detail}
        return JSONResponse(status_code=status_code, content=content, headers=exc.headers)

    return exception_handler


exception_handlers = [
    (EmployeeServiceError, status.HTTP_500_INTERNAL_SERVER_ERROR, "Internal Server Error"),
    (EmployeeNotFoundError, status.HTTP_404_NOT_FOUND, "Resource not found"),
    (EmployeeAlreadyExistsError, status.HTTP_409_CONFLICT, "Resource already exists"),
]

for exc_class, status_code, message in exception_handlers:
    app.add_exception_handler(
        exc_class_or_status_code=exc_class,
        handler=create_exception_handler(status_code, message)
    )
