from pydantic import BaseModel


class UserInSchema(BaseModel):
    username: str
    password: str


class UserSchema(UserInSchema):
    id: int

    class Config:
        orm_mode = True
