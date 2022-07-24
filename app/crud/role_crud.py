from tortoise.query_utils import QueryModifier as Q
from ..models.model import Role, UserRole


# 查询user_role
async def get_user_role(user_id: int|None=None, role_id: int|None=None):
    return UserRole.filter(Q(Q(user_id=user_id), Q(role_id=role_id))).all()


# 查询角色
async def get_role(role_id: int):
    return Role.filter(id=role_id).first()


# 查询角色
async def get_roles():
    return Role.filter().order_by('+id').all()


# 新增角色
async def create_role(role_name: str):
    return Role.create(role_name=role_name)


# 删除角色
async def delete_role(role_id: int):
    Role.filter(id=role_id).delete()
