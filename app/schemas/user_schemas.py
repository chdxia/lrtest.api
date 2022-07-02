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
