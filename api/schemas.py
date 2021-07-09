from decimal import Decimal
from typing import List, Optional

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


class ProductListSchema(ProductListShortSchema):
    products: List[ProductSchema] = []

    class Config:
        orm_mode = True
