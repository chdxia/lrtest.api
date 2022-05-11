from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import crud, models, schemas
from ..db.database import get_db
from ..dependencies import get_token_header


router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


# 获取用户信息
@router.get("/", response_model=list[schemas.User])
async def read_users(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    users= crud.get_users(db, skip=skip, limit=limit)
    return users


# 根据id获取用户信息
@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session=Depends(get_db)):
    db_user= crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


# 根据用户id获取商品
@router.get("/{user_id}/items", response_model=list[schemas.Item])
async def get_items_by_userid(user_id: int, db: Session=Depends(get_db)):
    db_items= crud.get_items_by_userid(db, user_id=user_id)
    if db_items is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_items


# 新增用户
@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user= crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="email already existed!")
    return crud.create_user(db=db, user=user)


# 新增商品
@router.post("/{user_id}/items", response_model= schemas.Item)
async def create_item_for_user(
    user_id: int,
    item: schemas.ItemCreate,
    db: Session=Depends(get_db)
):
    db_user= crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=400, detail="user not exist!")
    return crud.create_user_item(db=db, item=item, user_id=user_id)