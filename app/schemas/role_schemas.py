from pydantic import BaseModel


# 新增角色
class RoleCreate(BaseModel):
    role_name: str

# 角色
class Role(BaseModel):
    id: int
    role_name: str
    class Config:
        orm_mode = True

# 返回角色信息
class RoleResponse(BaseModel):
    code: int
    message: str
    data: Role

# 角色数量
class RoleTotal(BaseModel):
    total: int
    roles: list[Role]

# 返回角色信息
class RolesResponse(BaseModel):
    code: int
    message: str
    data: RoleTotal
