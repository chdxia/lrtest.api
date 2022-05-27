from sre_constants import GROUPREF_EXISTS
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import crud, models, schemas
from ..db.database import get_db
from ..dependencies import get_token_header
from ..utils.log_settings import logger


router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


# 查询用户
@router.get("/", response_model=list[schemas.User])
async def get_users(email: str|None=None, skip: int=0, limit: int=10, db: Session=Depends(get_db)):
    logger.info(type(email))
    if email is None:
        db_user = crud.get_users(db, skip=skip, limit=limit)
    else:
        db_user = crud.get_user_by_email(db, email=email, skip=skip, limit=limit)
    logger.info("查询用户信息")
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user


# 根据id查询用户
@router.get("/{user_id}", response_model=schemas.User)
async def read_user(user_id: int, db: Session=Depends(get_db)):
    db_user= crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return db_user


# 根据用户id查询物品
@router.get("/{user_id}/items", response_model=list[schemas.Item])
async def get_items_by_userid(user_id: int, db: Session=Depends(get_db)):
    db_items= crud.get_items_by_userid(db, user_id=user_id)
    if db_items is None:
        raise HTTPException(status_code=404, detail="item not found")
    return db_items


# 新增用户
@router.post("/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user= crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="email already existed!")
    return crud.create_user(db=db, user=user)


#修改用户
@router.put('/{user_id}', response_model=schemas.User)
async def update_user(user_id: int, user: schemas.UserUpdate, db:Session=Depends(get_db)):
    db_user= crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return crud.update_user(db, user=user, user_id=user_id)


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