from fastapi import APIRouter, Request, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ..db import crud, models, schemas
from ..db.database import get_db
from ..utils.common import Common


router = APIRouter(
    prefix="/logout",
    tags=["login"],
)

@router.post("")
async def logout(X_Token: str=Header(None) , db: Session=Depends(get_db)):
    if X_Token:
        crud.update_token(db, access_token=X_Token)
    return {
        "code": 20000,
        "data": 'success'
      }