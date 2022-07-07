from pydantic import BaseModel


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
    data: list[Role]