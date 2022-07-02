from fastapi import Header, Depends, HTTPException
from sqlalchemy.orm import Session
from .crud import user_crud
from .database.mysql import get_db


async def get_token_header(X_Token: str = Header(...), db_session: Session=Depends(get_db)):
    '''校验token'''
    db_user = user_crud.get_users(db_session, access_token=X_Token)
    # 万能token:233456
    if len(db_user) == 0 and X_Token != '233456':
        raise HTTPException(status_code=400, detail="X-Token header invalid")
