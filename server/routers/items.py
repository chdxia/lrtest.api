from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import crud, models, schemas
from ..db.database import get_db
from ..dependencies import get_token_header


router = APIRouter(
    prefix="/items",
    tags=["items"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


# 获取商品信息
@router.get("/", response_model=list[schemas.Item])
async def read_items(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    items= crud.get_items(db, skip=skip, limit=limit)
    return items


# 根据id查询商品信息
@router.get("/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int, db: Session=Depends(get_db)):
    db_item= crud.get_item_by_id(db, item_id= item_id)
    if item_id is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


# 更新商品信息
@router.put(
    "/{item_id}",
    response_model= schemas.Item,
    responses={403: {"description": "Operation forbidden"}}
)
async def update_item(item_id: int, item: schemas.ItemUpdate, db: Session=Depends(get_db)):
    db_item= crud.get_item_by_id(db, item_id= item_id)
    db_user= crud.get_user_by_id(db, user_id=item.owner_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="item not exist!")
    elif db_user is None:
        raise HTTPException(status_code=404, detail="user not exist!")
    return crud.update_item(db, item=item, item_id=item_id)