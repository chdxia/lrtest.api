from ..models.models import Role, UserRole


# 查询user_role
async def get_user_role(user_id: int|None=None, role_id: int|None=None):
    return await UserRole.filter(user_id=user_id, role_id=role_id).values()


# 查询角色
async def get_role(role_id: int):
    return await Role.filter(id=role_id).first().values()


# 查询角色
async def get_roles():
    return await Role.filter().order_by('id').values()


# 新增角色
async def create_role(role_name: str):
    a = await Role.create(role_name=role_name)
    print(type(a))
    print(a)
    return a


# 删除角色
async def delete_role(role_id: int):
    return await Role.filter(id=role_id).delete()
