from ..models.models import Role, UserRole


# 查询user_role
async def get_user_role(user_id: int|None=None, role_id: int|None=None):
    query = {'user_id':user_id, 'role_id':role_id}
    query_ignore_none = {key: value for key, value in query.items() if value is not None}
    return await UserRole.filter(**query_ignore_none).values()


# 查询角色
async def get_role(role_id: int):
    return await Role.filter(id=role_id).first()


# 查询角色
async def get_roles(page: int|None=1, limit: int|None=10):
    filters = Role.filter().order_by('id')
    total = await filters.count()
    filters_page_limit = await filters.offset((page-1)*limit).limit(limit)
    return {'total':total, 'roles':filters_page_limit}


# 新增角色
async def create_role(role_name: str):
    return await Role.create(role_name=role_name)


# 删除角色
async def delete_role(role_id: int):
    return await Role.filter(id=role_id).delete()
