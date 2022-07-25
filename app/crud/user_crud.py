import uuid
from ..models.models import User, UserRole
from ..schemas import user_schemas
from ..lib import str_to_sha256


# 查询用户
async def get_user(
    user_id: int|None=None,
    account: str|None=None,
    email: str|None=None,
    access_token: str|None=None
):
    return await User.filter(
        id=user_id,
        account=account,
        email=email,
        access_token=access_token
    ).first().values()


# 查询用户
async def get_users(
    account: str|None=None,
    user_name: str|None=None,
    email: str|None=None,
    access_token: str|None=None,
    role_id: int|None=None,
    status: bool|None=None,
    sort: str|None = 'create_time'
):
    return await User.filter(
        account__contains = account,
        user_name__contains = user_name,
        email__contains = email,
        access_token = access_token,
        id__in = list(map(lambda item: item.user_id, await UserRole.filter(id = role_id).values())),
        status = status
    ).order_by(sort).values()


# 新增用户
async def create_user(user: user_schemas.UserCreate):
    db_user = await User.create(
        account = user.account,
        user_name = user.user_name,
        email = user.email,
        password = str_to_sha256(user.password),
        status = user.status
    )
    if user.roles:
        for item in user.roles:
            await UserRole.create(user_id='1', role_id='1')
    return db_user


# 修改用户
async def update_user(user:user_schemas.UserUpdate, user_id: int):
    await UserRole.filter(user_id=user_id).delete()
    db_user = await User.filter(id=user_id).update(
        account = user.account,
        user_name = user.user_name,
        email = user.email,
        status = user.status
    )
    if user.password:
        db_user = await User.filter(id=user_id).update(password = str_to_sha256(user.password))
    if user.roles:
        for item in user.roles:
            await UserRole.create(user_id=user_id, role_id=item)
    return db_user


# 删除用户
async def delete_user(user_id: int):
    await UserRole.filter(user_id=user_id).delete()
    await User.filter(id=user_id).delete()


# 更新token
async def update_token(user_id: int|None=None, access_token: str|None=None):
    '''
    更新token

    传入user_id时，更新该用户的token，返回token值

    没有传入user_id，且传入token时，删除该token值（此处暂未考虑token重复）
    '''
    if user_id:
        token = uuid.uuid4()
        await User.filter(id=user_id).update(access_token=token)
        return token
    elif access_token:
        await User.filter(access_token=access_token).update(access_token = None)
