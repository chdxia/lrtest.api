from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from ..database.mysql import get_db
from ..crud import user_crud
from ..schemas import user_schemas
from ..utils.common import str_to_selt_sha256


router = APIRouter(
    tags=["登录"]
)

@router.post("/login", summary='登录')
async def login(body: user_schemas.UserLogin, db_session: Session=Depends(get_db)):
    db_user = user_crud.get_user_by_email(db_session, email=body.email)
    if db_user is None:
        raise HTTPException(status_code=400, detail="email or password is incorrect")
    elif db_user.password == str_to_selt_sha256(body.password, db_user.password.split('$')[2]):
        return {"code": 20000, "message": "success", "data":{"token": user_crud.update_token(db_session, db_user.id)}}
    else:
        raise HTTPException(status_code=400, detail="email or password is incorrect")


@router.delete("/logout", summary='退出登录')
async def logout(X_Token: str=Header(None) , db_session: Session=Depends(get_db)):
    if X_Token:
        user_crud.update_token(db_session, access_token=X_Token)
    return {"code": 20000, "message": "success"}
