from datetime import datetime
from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class ItemUpdate(ItemBase):
    owner_id: int


class Item(ItemBase):
    id: int
    owner_id: int
    createtime: datetime
    updatetime: datetime
    
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    createtime: datetime
    updatetime: datetime
    items: list[Item] = []

    class Config:
        orm_mode = True
