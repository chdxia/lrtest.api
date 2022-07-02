from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.mysql import get_db
from ..crud import user_crud, item_crud
from ..schemas import item_schemas


router = APIRouter(
    prefix="/items",
    tags=["物品"]
)


@router.get("", response_model=item_schemas.ItemsResponse, summary='查询物品')
async def read_items(title: str|None=None, description: str|None=None, page: int=1, limit: int=10, db_session: Session=Depends(get_db)):
    db_items = item_crud.get_items(db_session, title=title, description=description)
    paginated_items = list(db_items)[(page-1)*limit:(page-1)*limit+limit]
    return {"code": 20000, "message": "success", "data": paginated_items}


@router.get("/{item_id}", response_model=item_schemas.ItemResponse, summary='根据id查询物品')
async def read_item(item_id: int, db_session: Session=Depends(get_db)):
    db_item = item_crud.get_item_by_id(db_session, item_id)
    if item_id is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"code": 20000, "message": "success", "data": db_item}


@router.put("/{item_id}", response_model= item_schemas.ItemResponse, responses={403: {"description": "Operation forbidden"}}, summary='修改物品')
async def update_item(item_id: int, item: item_schemas.ItemUpdate, db_session: Session=Depends(get_db)):
    db_item= item_crud.get_item_by_id(db_session, item_id)
    db_user= user_crud.get_user_by_id(db_session, user_id=item.owner_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="item not found")
    elif db_user is None:
        raise HTTPException(status_code=404, detail="user not found")
    return {"code": 20000, "message": "success", "data": item_crud.update_item(db_session, item, item_id)}
