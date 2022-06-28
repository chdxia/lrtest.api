from datetime import datetime
from pydantic import BaseModel


class UserLogin(BaseModel):
    '''用户登录'''
    email: str
    password: str

class UserCreate(UserLogin):
    '''创建用户'''
    name: str|None=None
    role: int
    status: bool

class UserUpdate(UserCreate):
    '''修改用户'''
    password: str|None=None

class User(BaseModel):
    '''用户信息'''
    id: int
    name: str|None=None
    email: str
    role: int
    status: bool
    create_time: datetime
    update_time: datetime
    class Config:
        orm_mode = True

class UserResponse(BaseModel):
    '''返回用户信息'''
    code: int
    message: str
    data: User

class UserTotal(BaseModel):
    '''用户数量'''
    total: int
    users: list[User]

class UsersResponse(BaseModel):
    '''返回用户信息'''
    code: int
    message: str
    data: UserTotal


class ItemBase(BaseModel):
    '''物品'''
    title: str|None=None
    description: str|None=None

class ItemCreate(ItemBase):
    '''新增物品'''

class ItemUpdate(ItemBase):
    '''修改物品'''

class Item(BaseModel):
    '''物品信息'''
    id: int
    title: str
    description: str
    owner_id: int
    create_time: datetime
    update_time: datetime
    class Config:
        orm_mode = True

class ItemResponse(BaseModel):
    '''返回物品信息'''
    code: int
    message: str
    data: Item

class ItemsResponse(BaseModel):
    '''返回物品信息'''
    code: int
    message: str
    data: list[Item]


class FileCreate(BaseModel):
    '''新建七牛链接'''
    key: str

class FilesResponse(BaseModel):
    '''返回七牛链接'''
    code: int
    message: str
    data: list
