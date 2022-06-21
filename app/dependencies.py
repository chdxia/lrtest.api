from fastapi import Header, Depends, HTTPException
from sqlalchemy.orm import Session
from .db import crud
from .db.database import get_db


async def get_token_header(X_Token: str = Header(...), db_session: Session=Depends(get_db)):
    '''校验token'''
    db_user = crud.get_users(db_session, access_token=X_Token)
    # 万能token:233456
    if len(db_user) == 0 and X_Token != '233456':
        raise HTTPException(status_code=400, detail="X-Token header invalid")
