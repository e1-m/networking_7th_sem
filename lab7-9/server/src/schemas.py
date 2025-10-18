from pydantic import BaseModel


class IdResponse(BaseModel):
    id: int


class PublicKeyResponse(BaseModel):
    public_key: str


class MessageIn(BaseModel):
    message: str


class MessageOut(BaseModel):
    message: str
