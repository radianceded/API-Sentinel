from datetime import datetime

from typing import Annotated

from pydantic import BaseModel, ConfigDict, StringConstraints


Username = Annotated[
    str,
    StringConstraints(strip_whitespace=True, min_length=3, max_length=50),
]
Password = Annotated[str, StringConstraints(min_length=6, max_length=128)]


class UserCreate(BaseModel):
    username: Username
    password: Password


class UserLogin(BaseModel):
    username: Username
    password: Password


class UserOut(BaseModel):
    id: int
    username: str
    role: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
