from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import crud, models, schemas
from ..db.database import get_db
from ..utils.common import Common


router = APIRouter(
    prefix="/items",
    tags=["items"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}}
)


# 查询物品
@router.get("", response_model=schemas.Items)
async def read_items(title: str|None=None, description: str|None=None, page: int=1, limit: int=10, db: Session=Depends(get_db)):
    items= crud.get_items(db, title=title, description=description, skip=Common.page_to_skip(page, limit), limit=limit)
    return items


# 根据id查询物品
@router.get("/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int, db: Session=Depends(get_db)):
    db_item= crud.get_item_by_id(db, item_id= item_id)
    if item_id is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


# 修改物品
@router.put(
    "/{item_id}",
    response_model= schemas.Item,
    responses={403: {"description": "Operation forbidden"}}
)
async def update_item(item_id: int, item: schemas.ItemUpdate, db: Session=Depends(get_db)):
    db_item= crud.get_item_by_id(db, item_id= item_id)
    db_user= crud.get_user_by_id(db, user_id=item.owner_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="item not found")
    elif db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return crud.update_item(db, item=item, item_id=item_id)