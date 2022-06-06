from sre_constants import SUCCESS
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import crud, schemas
from ..db.database import get_db
from ..utils.log_settings import logger
from ..utils.common import Common
from typing import Union


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}}
)


# 查询用户
@router.get("", response_model=schemas.responseUsers, summary='查询用户')
async def get_users(
    name: str|None=None,
    email: str|None=None,
    role: int|None = None,
    status: bool|None=None,
    page: int=1,
    limit: int=10,
    sort: str|None=None,
    db: Session=Depends(get_db)
):
    db_user = crud.get_users(db, name=name, email=email, role=role, status=status, sort=sort)
    paginated_user = list(db_user)[(page-1)*limit:(page-1)*limit+limit]
    logger.info("查询用户")
    return {"code": 20000, "data": dict({"total":len(list(db_user)), "users":paginated_user})}


# 获取当前用户信息
@router.get("/info")
async def get_info():
    return {
        "code":20000,
        "data":{
            "roles":["admin"],
            "introduction":"I am a super administrator",
            "avatar":"https://wpimg.wallstcn.com/f778738c-e4f8-4870-b634-56703b4acafe.gif",
            "name":"Super Admin"
        }
    }


# 根据id查询用户
@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session=Depends(get_db)):
    db_user= crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user


# 根据用户id查询物品
@router.get("/{user_id}/items", response_model=list[schemas.Item])
async def get_items_by_userid(user_id: int, title: str|None=None, description: str|None=None, page: int=1, limit: int=10, db: Session=Depends(get_db)):
    db_items= crud.get_items(db, user_id=user_id, title=title, description=description, skip=Common.page_to_skip(page, limit), limit=limit)
    return db_items


# 新增用户
@router.post("", response_model=schemas.responseUser)
async def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    # 验证邮箱是否已存在
    db_user= crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="email already existed!")
    return {"code": 20000, "data": crud.create_user(db=db, user=user)}


#修改用户
@router.put('/{user_id}', response_model=schemas.responseUser)
async def update_user(user_id: int, user: schemas.UserUpdate, db:Session=Depends(get_db)):
    db_user= crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return {"code": 20000, "data": crud.update_user(db, user=user, user_id=user_id)}


# 删除用户
@router.delete('/{user_id}', response_model=schemas.responseUser)
async def delete_user(user_id: int, db:Session=Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    crud.delete_user(db, user_id=user_id)
    return {"code": 20000, "data": db_user}


# 新增物品
@router.post("/{user_id}/items", response_model= schemas.Item)
async def create_item_for_user(
    user_id: int,
    item: schemas.ItemCreate,
    db: Session=Depends(get_db)
):
    db_user= crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="user not found")
    return crud.create_user_item(db=db, item=item, user_id=user_id)