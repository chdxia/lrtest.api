from datetime import datetime
from pydantic import BaseModel


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