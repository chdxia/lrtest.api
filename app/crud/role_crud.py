from tortoise.query_utils import Q
from ..models.model import Role, UserRole


# 查询user_role
def get_user_role(user_id: int|None=None, role_id: int|None=None):
    return UserRole.filter(Q(Q(user_id=user_id), Q(role_id=role_id))).all()


# 查询角色
def get_role(role_id: int):
    return Role.filter(id=role_id).first()


# 查询角色
def get_roles():
    return Role.filter().order_by('+id').all()


# 新增角色
def create_role(role_name: str):
    return Role.create(role_name=role_name)


# 删除角色
def delete_role(role_id: int):
    Role.filter(id=role_id).delete()
