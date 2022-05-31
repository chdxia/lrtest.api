from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import crud, models, schemas
from ..db.database import get_db
from ..utils.common import Common


router = APIRouter()

@router.post("/login", tags=["login"])
async def login(body: schemas.UserCreate, db: Session=Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=body.email)
    password = db_user.password.split('$')
    if db_user is None:
        raise HTTPException(status_code=400, detail="email or password is incorrect")
    elif db_user.password == Common.str_to_selt_sha256(body.password, password[2]):
        return {"token": crud.update_token(db, db_user.id)}
    else:
        raise HTTPException(status_code=400, detail="email or password is incorrect")