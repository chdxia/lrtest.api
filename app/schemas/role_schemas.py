from pydantic import BaseModel


class RoleCreate(BaseModel):
    '''新增角色'''
    role_name: str

class Role(BaseModel):
    '''角色'''
    id: int
    role_name: str
    class Config:
        orm_mode = True

class RoleResponse(BaseModel):
    '''返回角色信息'''
    code: int
    message: str
    data: Role

class RoleTotal(BaseModel):
    '''角色数量'''
    total: int
    roles: list[Role]

class RolesResponse(BaseModel):
    '''返回角色信息'''
    code: int
    message: str
    data: RoleTotal