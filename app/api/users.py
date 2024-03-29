import re
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from tortoise.expressions import Q
from ..models.models import User, UserRole
from ..schemas import user_schemas
from ..dependencies import role_depends
from ..utils import ignore_none, str_to_sha256


router = APIRouter(prefix='/users', tags=['用户'])


@router.get('', response_model=user_schemas.UsersResponse, summary='查询用户', dependencies=[Depends(role_depends())])
async def get_users(
    account: str|None=None,
    user_name: str|None=None,
    email: str|None=None,
    role_id: int|None=None,
    status: bool|None=None,
    sort: str|None='create_time',
    page: int|None=1,
    limit: int|None=10
):
    db_user = User.filter(**ignore_none(
        account__contains = account,
        user_name__contains = user_name,
        email__contains = email,
        id__in = list(map(lambda item: item['user_id'], await UserRole.filter(role_id = role_id).values())) if role_id else None,
        status = status
    )).order_by(sort)
    return {
        "code": 200,
        "message": "success",
        "data": {
            "total": await db_user.count(),
            "users": await db_user.offset((page-1)*limit).limit(limit).prefetch_related('_roles', '_tasks')
        }
    }


@router.post('', response_model=user_schemas.UserResponse, summary='新增用户', dependencies=[Depends(role_depends('admin'))])
async def create_user(user: user_schemas.UserCreate):
    if re.fullmatch(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', user.account): # 账号正则，不能使用邮箱
        raise HTTPException(status_code=400, detail='账号格式错误')
    if not re.fullmatch(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', user.email): # 邮箱正则
        raise HTTPException(status_code=400, detail='邮箱格式错误')
    if await User.filter(account=user.account).first(): # 验证账号是否已存在
        raise HTTPException(status_code=400, detail=f'账号({user.account})已存在')
    if await User.filter(email=user.email).first(): # 验证邮箱是否已存在
        raise HTTPException(status_code=400, detail=f'邮箱({user.email})已存在')
    # 创建用户
    db_user = await User.create(
        account = user.account,
        user_name = user.user_name,
        email = user.email,
        password = str_to_sha256(user.password),
        status = user.status,
        create_time = datetime.now(),
        update_time = datetime.now()
    )
    # 用户、角色之间的绑定
    [await UserRole.create(user_id=db_user.id, role_id=item) for item in user.roles if user.roles]
    return {"code": 200, "message": "success", "data": await User.filter(id=db_user.id).first().prefetch_related('_roles', '_tasks')}


@router.get('/{user_id}', response_model=user_schemas.UserResponse, summary='根据id查询用户', dependencies=[Depends(role_depends())])
async def read_user(user_id: int):
    db_user = await User.filter(id=user_id).first().prefetch_related('_roles', '_tasks')
    if not db_user:
        raise HTTPException(status_code=404, detail='user not found')
    return {"code": 200, "message": "success", "data": db_user}


@router.put('/{user_id}', response_model=user_schemas.UserResponse, summary='修改用户', dependencies=[Depends(role_depends('admin'))])
async def update_user(user_id: int, user: user_schemas.UserUpdate):
    db_user = await User.filter(id=user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail=f'user ({user.account}) not found')
    if re.fullmatch(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', user.account):
        raise HTTPException(status_code=400, detail='account is incorrect')
    if not re.fullmatch(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$', user.email):
        raise HTTPException(status_code=400, detail='email is incorrect')
    db_user_account_email = await User.filter(Q(account=user.account) | Q(email=user.email)).first()
    if db_user_account_email and db_user_account_email != db_user:
        raise HTTPException(status_code=400, detail='账号或邮箱已存在')
    await UserRole.filter(user_id=user_id).delete()
    await User.filter(id=user_id).update(
        account = user.account,
        user_name = user.user_name,
        email = user.email,
        status = user.status,
        update_time = datetime.now()
    )
    if user.password:
        await User.filter(id=user_id).update(password = str_to_sha256(user.password))
    [await UserRole.create(user_id=user_id, role_id=item) for item in user.roles if user.roles]
    return {"code": 200, "message": "success", "data": await User.filter(id=user_id).first().prefetch_related('_roles', '_tasks')}


@router.delete('/{user_id}', summary='删除用户', dependencies=[Depends(role_depends('admin'))])
async def delete_user(user_id: int):
    if not await User.filter(id=user_id).first():
        raise HTTPException(status_code=404, detail='user not found')
    if await User.filter(id=user_id).delete():
        return {"code": 200, "message": "success"}
