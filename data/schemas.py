from datetime import datetime

from pydantic import BaseModel


class UserModel:
    class UserCreateModel(BaseModel):
        username: str
        fullname: str
        password: str


class MessageModel(BaseModel):
    content: str
    sender: str
    receiver: str
    timestamp: datetime | None


class TokenModel(BaseModel):
    access_token: str
    token_type: str
