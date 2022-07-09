import re
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..exception.apiexception import ApiException
from ..database.mysql import get_mysql_db
from ..crud import user_crud
from ..schemas import user_schemas
from ..permission import role_depends


router = APIRouter(
    prefix="/users",
    tags=["用户"]
)


@router.get("", response_model=user_schemas.UsersResponse, summary='查询用户', dependencies=[Depends(role_depends())])
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


@router.post("", response_model=user_schemas.UserResponse, summary='新增用户', dependencies=[Depends(role_depends('admin'))])
async def create_user(user: user_schemas.UserCreate, db_session: Session=Depends(get_mysql_db)):
    if user_crud.get_user_by_account(db_session, account=user.account): # 验证账号是否已存在
        raise ApiException(status_code=200, content={"code": 40000, "message": "account already existed"})
    if user_crud.get_user_by_email(db_session, email=user.email): # 验证邮箱是否已存在
        raise ApiException(status_code=200, content={"code": 40000, "message": "email already existed"})
    if re.fullmatch(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', user.account): # 账号正则，不能使用邮箱
        raise ApiException(status_code=200, content={"code": 40000, "message": "account is incorrect"})
    if not re.fullmatch(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', user.email): # 邮箱正则
        raise ApiException(status_code=200, content={"code": 40000, "message": "email is incorrect"})
    return {"code": 20000, "message": "success", "data": user_crud.create_user(db_session, user)}


@router.get("/info", summary='查询当前用户信息', dependencies=[Depends(role_depends())])
async def get_info():
    return {
        "code": 20000,
        "message": "success",
        "data":{
            "roles":["admin"],
            "introduction":"I am a super administrator",
            "avatar":"http://qiniu.chdxia.com/FlVMejpFxswVqGscbaQwDRn2r1jr",
            "name":"chdxia"
        }
    }


@router.get("/{user_id}", response_model=user_schemas.UserResponse, summary='根据id查询用户', dependencies=[Depends(role_depends())])
async def read_user(user_id: int, db_session: Session=Depends(get_mysql_db)):
    db_user= user_crud.get_user_by_id(db_session, user_id)
    if db_user is None:
        raise ApiException(status_code=200, content={"code": 40000, "message": "user not found"})
    return {"code": 20000, "message": "success", "data": db_user}


@router.put('/{user_id}', response_model=user_schemas.UserResponse, summary='修改用户', dependencies=[Depends(role_depends('admin'))])
async def update_user(user_id: int, user: user_schemas.UserUpdate, db_session:Session=Depends(get_mysql_db)):
    db_user= user_crud.get_user_by_id(db_session, user_id)
    if db_user is None:
        raise ApiException(status_code=200, content={"code": 40000, "message": "user not found"})
    return {"code": 20000, "message": "success", "data": user_crud.update_user(db_session, user, user_id)}


@router.delete('/{user_id}', response_model=user_schemas.UserResponse, summary='删除用户', dependencies=[Depends(role_depends('admin'))])
async def delete_user(user_id: int, db_session:Session=Depends(get_mysql_db)):
    db_user = user_crud.get_user_by_id(db_session, user_id)
    if db_user is None:
        raise ApiException(status_code=200, content={"code": 40000, "message": "user not found"})
    user_crud.delete_user(db_session, user_id)
    return {"code": 20000, "message": "success", "data": db_user}
