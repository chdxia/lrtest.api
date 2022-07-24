from fastapi import APIRouter, HTTPException, Depends, Header
from tortoise.query_utils import QueryModifier as Q
from ..models.model import User
from ..crud import user_crud
from ..schemas import user_schemas
from ..dependencies import role_depends
from ..lib import str_to_selt_sha256


router = APIRouter(
    tags=['登录']
)


@router.post('/login', summary='登录')
async def login(body: user_schemas.UserLogin):
    # 支持账号/邮箱登录
    db_user = User.filter(Q(Q(account=body.account), Q(email=body.account), join_type="OR")).first()
    if db_user is None: # 账号/邮箱登录失败
        raise HTTPException(status_code=400, detail='Account or password is incorrect')
    elif not db_user.status: # 账户已停用
        raise HTTPException(status_code=400, detail='Account is disabled')
    elif db_user.password == str_to_selt_sha256(body.password, db_user.password.split('$')[2]): # 密码正确，更新token
        return {"code": 200, "message": "success", "data":{"token": user_crud.update_token(user_id=db_user.id)}}
    else:
        raise HTTPException(status_code=400, detail='Account or password is incorrect')


@router.delete('/logout', summary='退出登录', dependencies=[Depends(role_depends())])
async def logout(X_Token: str=Header(None)):
    if X_Token: # 清空token
        user_crud.update_token(access_token=X_Token)
    return {"code": 200, "message": "success"}
