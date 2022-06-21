from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import crud, schemas
from ..db.database import get_db


router = APIRouter(
    prefix="/users",
    tags=["用户"]
)


@router.get("", response_model=schemas.UsersResponse, summary='查询用户')
async def get_users(
    name: str|None=None,
    email: str|None=None,
    role: int|None=None,
    status: bool|None=None,
    page: int=1,
    limit: int=10,
    sort: str|None='+create_time',
    db_session: Session=Depends(get_db)
):
    '''查询用户'''
    db_user = crud.get_users(db_session, name, email, role, status, sort)
    paginated_users = list(db_user)[(page-1)*limit:(page-1)*limit+limit]
    return {"code": 20000, "message": "success", "data": dict({"total":len(list(db_user)), "users":paginated_users})}


@router.post("", response_model=schemas.UserResponse, summary='新增用户')
async def create_user(user: schemas.UserCreate, db_session: Session=Depends(get_db)):
    '''新增用户'''
    # 验证邮箱是否已存在
    db_user= crud.get_user_by_email(db_session, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="email already existed!")
    return {"code": 20000, "message": "success", "data": crud.create_user(db_session, user)}


@router.get("/info", summary='查询当前用户信息')
async def get_info():
    '''查询当前用户信息'''
    return {
        "code": 20000,
        "message": "success",
        "data":{
            "roles":["admin"],
            "introduction":"I am a super administrator",
            "avatar":"http://qiniu.chdxia.com/FlVMejpFxswVqGscbaQwDRn2r1jr",
            "name":"chdxia"
        }
    }


@router.get("/{user_id}", response_model=schemas.UserResponse, summary='根据id查询用户')
async def read_user(user_id: int, db_session: Session=Depends(get_db)):
    '''根据id查询用户'''
    db_user= crud.get_user_by_id(db_session, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return {"code": 20000, "message": "success", "data": db_user}


@router.put('/{user_id}', response_model=schemas.UserResponse, summary='修改用户')
async def update_user(user_id: int, user: schemas.UserUpdate, db_session:Session=Depends(get_db)):
    '''修改用户'''
    db_user= crud.get_user_by_id(db_session, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return {"code": 20000, "message": "success", "data": crud.update_user(db_session, user, user_id)}


@router.delete('/{user_id}', response_model=schemas.UserResponse, summary='删除用户')
async def delete_user(user_id: int, db_session:Session=Depends(get_db)):
    '''删除用户'''
    db_user = crud.get_user_by_id(db_session, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    crud.delete_user(db_session, user_id)
    return {"code": 20000, "message": "success", "data": db_user}


@router.get("/{user_id}/items", response_model=schemas.ItemsResponse, summary='根据用户id查询物品')
async def get_items_by_userid(user_id: int, title: str|None=None, description: str|None=None, page: int=1, limit: int=10, db_session: Session=Depends(get_db)):
    '''根据用户id查询物品'''
    db_items= crud.get_items(db_session, user_id, title, description)
    paginated_items = list(db_items)[(page-1)*limit:(page-1)*limit+limit]
    return {"code": 20000, "message": "success", "data": paginated_items}


@router.post("/{user_id}/items", response_model= schemas.ItemResponse, summary='新增物品')
async def create_item_for_user(
    user_id: int,
    item: schemas.ItemCreate,
    db_session: Session=Depends(get_db)
):
    '''新增物品'''
    db_user= crud.get_user_by_id(db_session, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return {"code": 20000, "message": "success", "data": crud.create_user_item(db_session, item, user_id)}
