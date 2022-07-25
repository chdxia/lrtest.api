import re
from fastapi import APIRouter, HTTPException, Header, Depends
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
    page: int|None=None,
    limit: int|None=None,
    sort: str|None='create_time'
):
    db_user = await user_crud.get_users(
        account=account,
        user_name=user_name,
        email=email,
        role_id=role_id,
        status=status,
        sort=sort,
        page=page,
        limit=limit
    )
    return {"code": 200, "message": "success", "data": db_user}


@router.post('', response_model=user_schemas.UserResponse, summary='新增用户', dependencies=[Depends(role_depends('admin'))])
async def create_user(user: user_schemas.UserCreate):
    if re.fullmatch(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', user.account): # 账号正则，不能使用邮箱
        raise HTTPException(status_code=400, detail='Account is incorrect')
    if not re.fullmatch(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', user.email): # 邮箱正则
        raise HTTPException(status_code=400, detail='Email is incorrect')
    if await user_crud.get_user(account=user.account): # 验证账号是否已存在
        raise HTTPException(status_code=400, detail=f'Account {user.account} already existed')
    if await user_crud.get_user(email=user.email): # 验证邮箱是否已存在
        raise HTTPException(status_code=400, detail=f'Email {user.email} already existed')
    return {"code": 201, "message": "success", "data": await user_crud.create_user(user)}


@router.get('/info', response_model=user_schemas.UserResponse, summary='查询当前用户信息', dependencies=[Depends(role_depends())])
async def get_info(X_Token: str = Header(...)):
    db_user = await user_crud.get_user(access_token=X_Token)
    if db_user is None:
        raise HTTPException(status_code=400, detail='X-Token header invalid')
    return {"code": 200, "message": "success", "data": db_user}


@router.get('/{user_id}', response_model=user_schemas.UserResponse, summary='根据id查询用户', dependencies=[Depends(role_depends())])
async def read_user(user_id: int):
    db_user = await user_crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return {"code": 200, "message": "success", "data": db_user}


@router.put('/{user_id}', response_model=user_schemas.UserResponse, summary='修改用户', dependencies=[Depends(role_depends('admin'))])
async def update_user(user_id: int, user: user_schemas.UserUpdate):
    db_user = await user_crud.get_user(user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail=f'User {user.account} not found')
    if re.fullmatch(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', user.account):
        raise HTTPException(status_code=400, detail='Account is incorrect')
    if not re.fullmatch(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', user.email):
        raise HTTPException(status_code=400, detail='Email is incorrect')
    db_user_account = user_crud.get_user(account=user.account)
    if db_user_account and db_user_account != db_user:
        raise HTTPException(status_code=400, detail=f'Account {user.account} already existed')
    db_user_email = user_crud.get_user(email=user.email)
    if db_user_email and db_user_email != db_user:
        raise HTTPException(status_code=400, detail=f'Email {user.email} already existed')
    if await user_crud.update_user(user, user_id):
        return {"code": 201, "message": "success", "data": db_user}
    else:
        raise HTTPException(status_code=500, detail='Failed to modify user')


@router.delete('/{user_id}', summary='删除用户', dependencies=[Depends(role_depends('admin'))])
async def delete_user(user_id: int):
    if user_crud.get_user(user_id=user_id) is None:
        raise HTTPException(status_code=404, detail='User not found')
    user_crud.delete_user(user_id)
    return {"code": 201, "message": "success"}
