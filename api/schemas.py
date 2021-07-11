from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, HttpUrl, validator


class UserCreateSchema(BaseModel):
    username: str
    password: str


class UserSchema(BaseModel):
    id: int
    username: str
    avatar: Optional[str]

    @validator("avatar", pre=True)
    def make_avatar_url(cls, v):
        if v:
            return f"/media/{v}"
        return v

    class Config:
        orm_mode = True


class PriceSchema(BaseModel):
    value: Decimal
    currency_code: str

    class Config:
        orm_mode = True


class ProductCreateSchema(BaseModel):
    sku: str
    name: str
    image_url: Optional[HttpUrl]

    prices: List[PriceSchema] = []


class ProductSchema(ProductCreateSchema):
    id: int

    class Config:
        orm_mode = True


class ProductListCreateSchema(BaseModel):
    name: Optional[str]
    products: List[ProductCreateSchema] = []


class ProductListShortSchema(BaseModel):
    id: int
    name: Optional[str]

    class Config:
        orm_mode = True


class ProductListSchema(ProductListShortSchema):
    products: List[ProductSchema] = []

    class Config:
        orm_mode = True


class ProductListResponseSchema(BaseModel):
    product_lists: List[ProductListShortSchema] = []

    class Config:
        orm_mode = True
