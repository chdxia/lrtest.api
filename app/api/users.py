import re
from fastapi import APIRouter, HTTPException, Header, Depends
from sqlalchemy.orm import Session
from ..database.mysql import get_mysql_db
from ..crud import user_crud
from ..schemas import user_schemas
from ..dependencies import role_depends


router = APIRouter(
    prefix='/users',
    tags=['用户']
)


@router.get('', response_model=user_schemas.UsersResponse, summary='查询用户', dependencies=[Depends(role_depends())])
async def get_users(
    account: str|None=None,
    user_name: str|None=None,
    email: str|None=None,
    role_id: int|None=None,
    status: bool|None=None,
    page: int=1,
    limit: int=10,
    sort: str|None='+create_time',
    db_session: Session=Depends(get_mysql_db)
):
    db_user = user_crud.get_users(db_session, account=account, user_name=user_name, email=email, role_id=role_id, status=status, sort=sort)
    paginated_users = list(db_user)[(page-1)*limit:(page-1)*limit+limit]
    return {"code": 20000, "message": "success", "data": dict({"total":len(list(db_user)), "users":paginated_users})}


@router.post('', response_model=user_schemas.UserResponse, summary='新增用户', dependencies=[Depends(role_depends('admin'))])
async def create_user(user: user_schemas.UserCreate, db_session: Session=Depends(get_mysql_db)):
    if re.fullmatch(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', user.account): # 账号正则，不能使用邮箱
        raise HTTPException(status_code=400, detail='Account is incorrect')
    if not re.fullmatch(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', user.email): # 邮箱正则
        raise HTTPException(status_code=400, detail='Email is incorrect')
    if user_crud.get_user_by_account(db_session, account=user.account): # 验证账号是否已存在
        raise HTTPException(status_code=400, detail='Account already existed')
    if user_crud.get_user_by_email(db_session, email=user.email): # 验证邮箱是否已存在
        raise HTTPException(status_code=400, detail='Email already existed')
    return {"code": 20000, "message": "success", "data": user_crud.create_user(db_session, user)}


@router.get('/info', response_model=user_schemas.UserResponse, summary='查询当前用户信息', dependencies=[Depends(role_depends())])
async def get_info(X_Token: str = Header(...), db_session: Session=Depends(get_mysql_db)):
    db_user = user_crud.get_user_by_token(db_session, access_token=X_Token)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return {"code": 20000, "message": "success", "data": db_user}


@router.get('/{user_id}', response_model=user_schemas.UserResponse, summary='根据id查询用户', dependencies=[Depends(role_depends())])
async def read_user(user_id: int, db_session: Session=Depends(get_mysql_db)):
    db_user = user_crud.get_user_by_id(db_session, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return {"code": 20000, "message": "success", "data": db_user}


@router.put('/{user_id}', response_model=user_schemas.UserResponse, summary='修改用户', dependencies=[Depends(role_depends('admin'))])
async def update_user(user_id: int, user: user_schemas.UserUpdate, db_session:Session=Depends(get_mysql_db)):
    db_user = user_crud.get_user_by_id(db_session, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    if re.fullmatch(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', user.account):
        raise HTTPException(status_code=400, detail='Account is incorrect')
    if not re.fullmatch(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', user.email):
        raise HTTPException(status_code=400, detail='Email is incorrect')
    db_user_account = user_crud.get_user_by_account(db_session, account=user.account)
    if db_user_account and db_user_account != db_user:
        raise HTTPException(status_code=400, detail='Account already existed')
    db_user_email = user_crud.get_user_by_email(db_session, email=user.email)
    if db_user_email and db_user_email != db_user:
        raise HTTPException(status_code=400, detail='Email already existed')
    return {"code": 20000, "message": "success", "data": user_crud.update_user(db_session, user, user_id)}


@router.delete('/{user_id}', summary='删除用户', dependencies=[Depends(role_depends('admin'))])
async def delete_user(user_id: int, db_session:Session=Depends(get_mysql_db)):
    if user_crud.get_user_by_id(db_session, user_id) is None:
        raise HTTPException(status_code=404, detail='User not found')
    user_crud.delete_user(db_session, user_id)
    return {"code": 20000, "message": "success"}
