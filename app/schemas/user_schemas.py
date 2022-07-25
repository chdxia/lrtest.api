from datetime import datetime
from pydantic import BaseModel


# 用户登录
class UserLogin(BaseModel):
    account: str
    password: str

# 新增用户
class UserCreate(UserLogin):
    user_name: str|None=None
    email: str
    roles: list
    status: bool

# 修改用户
class UserUpdate(UserCreate):
    password: str|None=None

# 用户的角色
class UserRole(BaseModel):
    id: int
    user_id: int
    role_id: int
    class Config:
        orm_mode = True

# 用户信息
class User(BaseModel):
    id: int
    account: str
    user_name: str|None=None
    email: str
    status: bool
    create_time: datetime
    update_time: datetime
    class Config:
        orm_mode = True

# 返回用户信息
class UserResponse(BaseModel):
    code: int
    message: str
    data: User

# 用户数量
class UserTotal(BaseModel):
    total: int
    users: list[User]

# 返回用户信息
class UsersResponse(BaseModel):
    code: int
    message: str
    data: UserTotal
