from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ..db import crud, schemas
from ..db.database import get_db
from ..utils.common import Common


router = APIRouter(
    tags=["login"],
    responses={404: {"description": "Not found"}}
)

@router.post("/login")
async def login(body: schemas.UserLogin, db: Session=Depends(get_db)):  
    db_user = crud.get_user_by_email(db, email=body.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="email or password is incorrect")
    
    elif db_user.password == Common.str_to_selt_sha256(body.password, db_user.password.split('$')[2]):
        return {"code": 20000, "data":{"token": crud.update_token(db, db_user.id)}}
    
    else:
        raise HTTPException(status_code=400, detail="email or password is incorrect")


@router.post("/logout")
async def logout(X_Token: str=Header(None) , db: Session=Depends(get_db)):
    if X_Token:
        crud.update_token(db, access_token=X_Token)
    return {"code": 20000, "data": 'success'}