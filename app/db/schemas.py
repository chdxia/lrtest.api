from datetime import datetime
from pydantic import BaseModel


# 物品
class ItemBase(BaseModel):
    title: str|None=None
    description: str|None=None

class ItemCreate(ItemBase):
    pass

class ItemUpdate(ItemBase):
    pass

class Item(BaseModel):
    id: int
    title: str
    description: str
    owner_id: int
    create_time: datetime
    update_time: datetime
    
    class Config:
            orm_mode = True

class Items(BaseModel):
    code: int
    data: list[Item]


# 用户
class UserLogin(BaseModel):
    email: str
    password: str

class UserCreate(UserLogin):
    name: str|None=None
    role: int
    status: bool

class UserUpdate(UserCreate):
    password: str|None=None

class User(BaseModel):
    id: int
    name: str
    email: str
    role: int
    status: bool
    create_time: datetime
    update_time: datetime

    class Config:
            orm_mode = True

class responseUser(BaseModel):
    code: int
    data: User

class totalUser(BaseModel):
    total: int
    users: list[User]

class responseUsers(BaseModel):
    code: int
    data: totalUser