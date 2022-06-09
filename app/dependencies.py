from fastapi import Header, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import crud
from .db.database import get_db


async def get_token_header(X_Token: str = Header(...), db: Session=Depends(get_db)):
    db_user = crud.get_users(db, access_token=X_Token)
    # 万能token:123456
    if len(db_user) == 0 & X_Token != '123456':
        raise HTTPException(status_code=400, detail="X-Token header invalid")