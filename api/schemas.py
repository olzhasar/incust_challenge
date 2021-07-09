from typing import Optional

from pydantic import BaseModel, HttpUrl


class UserCreateSchema(BaseModel):
    username: str
    password: str
    avatar_url: Optional[HttpUrl]


class UserChangeSchema(BaseModel):
    username: Optional[str]
    avatar_url: Optional[HttpUrl]


class UserSchema(UserCreateSchema):
    id: int

    class Config:
        orm_mode = True
