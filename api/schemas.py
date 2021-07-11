from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, validator


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


class ProductBaseSchema(BaseModel):
    sku: str
    name: str
    prices: List[PriceSchema] = []


class ProductCreateSchema(ProductBaseSchema):
    product_list_id: int


class ProductSchema(ProductBaseSchema):
    id: int
    image: Optional[str]

    @validator("image", pre=True)
    def make_avatar_url(cls, v):
        if v:
            return f"/media/{v}"
        return v

    class Config:
        orm_mode = True


class ProductListCreateSchema(BaseModel):
    name: Optional[str]


class ProductListShortSchema(ProductListCreateSchema):
    id: int

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
