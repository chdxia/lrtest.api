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


@router.get("/", response_model=list[schemas.Item])
async def read_items(skip: int=0, limit: int=100, db: Session=Depends(get_db)):
    items= crud.get_items(db, skip=skip, limit=limit)
    return items


@router.get("/{item_id}", response_model=schemas.Item)
async def read_item(item_id: int, db: Session=Depends(get_db)):
    db_item= crud.get_item_by_id(db, item_id= item_id)
    if item_id is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.put(
    "/{item_id}",
    tags=["custom"],
    responses={403: {"description": "Operation forbidden"}},
)
async def update_item(item_id: str):
    if item_id != "plumbus":
        raise HTTPException(
            status_code=403, detail="You can only update the item: plumbus"
        )
    return {"item_id": item_id, "name": "The great Plumbus"}