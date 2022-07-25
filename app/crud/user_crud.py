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
    query = {'id':user_id, 'account':account, 'email':email, 'access_token':access_token}
    query_ignore_none = {key: value for key, value in query.items() if value is not None}
    return await User.filter(**query_ignore_none).first()


# 查询用户
async def get_users(
    account: str|None=None,
    user_name: str|None=None,
    email: str|None=None,
    access_token: str|None=None,
    role_id: int|None=None,
    status: bool|None=None,
    sort: str|None='create_time',
    page: int|None=1,
    limit: int|None=10
):
    query = {
        'account__contains': account,
        'user_name__contains': user_name,
        'email__contains': email,
        'access_token': access_token,
        'status': status
    }
    # 忽略查询参数中的None值
    query_ignore_none = {key: value for key, value in query.items() if value is not None}
    filters = User.filter(**query_ignore_none).filter(
        id__in = list(map(lambda item: item['user_id'], await UserRole.filter(role_id = role_id).values()))
    ).order_by(sort)
    # 用户列表页面中的total字段
    total = await filters.count()
    # 对查询结果进行分页
    filters_page_limit = await filters.offset((page-1)*limit).limit(limit)
    return {'total':total, 'users':filters_page_limit}


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
            await UserRole.create(user_id=db_user.id, role_id=item)
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
    return await User.filter(id=user_id).delete()


# 更新token
async def update_token(user_id: int|None=None, access_token: str|None=None):
    '''
    更新token

    传入user_id时，更新该用户的token，返回token值

    没有传入user_id，且传入token时，删除该token值（此处暂未考虑token重复）
    '''
    if user_id:
        token = uuid.uuid4()
        return await User.filter(id=user_id).update(access_token=token)
    elif access_token:
        return await User.filter(access_token=access_token).update(access_token = None)
