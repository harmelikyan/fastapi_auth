from dataclasses import dataclass
from pydantic import BaseModel, EmailStr


class User(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: int


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    admin: bool


class UserCreate(UserBase):
    password: str


class DBUser(UserBase):
    id: int
    email: EmailStr
    hashed_password: str

    items: list[Item] = []

    class Config:
        orm_mode = True
