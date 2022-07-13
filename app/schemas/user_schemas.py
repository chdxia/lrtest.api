from datetime import datetime
from pydantic import BaseModel


class UserLogin(BaseModel):
    '''用户登录'''
    account: str
    password: str

class UserCreate(UserLogin):
    '''创建用户'''
    user_name: str|None=None
    email: str
    roles: list
    status: bool

class UserUpdate(UserCreate):
    '''修改用户'''
    password: str|None=None

class UserRole(BaseModel):
    '''用户的角色'''
    id: int
    user_id: int
    role_id: int
    class Config:
        orm_mode = True

class User(BaseModel):
    '''用户信息'''
    id: int
    account: str
    user_name: str|None=None
    email: str
    roles: list[UserRole]
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
