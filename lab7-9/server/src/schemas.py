from pydantic import BaseModel


class PublicKeyResponse(BaseModel):
    key_id: str
    public_key: str


class SessionOut(BaseModel):
    session_id: str
    expires_at: int


class SessionIn(BaseModel):
    aes_key_b64_encrypted: str


class Session(BaseModel):
    session_id: str
    aes_key_b64: str
    expires_at: int


class MessageIn(BaseModel):
    message: str


class MessageOut(BaseModel):
    message: str
