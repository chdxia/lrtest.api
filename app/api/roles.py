from fastapi import APIRouter, HTTPException, Depends
from ..models.models import Role
from ..crud import role_crud
from ..schemas import role_schemas
from ..dependencies import role_depends


router = APIRouter(
    prefix='/roles',
    tags=['角色']
)


@router.get('', response_model=role_schemas.RolesResponse, summary='查询角色', dependencies=[Depends(role_depends())])
async def get_roles(page: int|None=None, limit: int|None=None):
    db_roles = await role_crud.get_roles(page=page, limit=limit)
    return {"code": 200, "message": "success", "data": db_roles}


@router.post('', response_model=role_schemas.RoleResponse, summary='新增角色', dependencies=[Depends(role_depends('admin'))])
async def create_role(role: role_schemas.RoleCreate):
    roles = list(map(lambda item: item['role_name'], await Role.all().values()))
    if role.role_name in roles:
        raise  HTTPException(status_code=400, detail=f'Role {role.role_name} already existed')
    return {"code": 201, "message": "success", "data": await role_crud.create_role(role_name=role.role_name)}


@router.delete('/{role_id}', summary='删除角色', dependencies=[Depends(role_depends('admin'))])
async def delete_role(role_id: int):
    db_role = await role_crud.get_role(role_id)
    if db_role is None:
        raise  HTTPException(status_code=404, detail='Role not found')
    elif db_role.role_name == 'admin':
        raise  HTTPException(status_code=401, detail='Not allowed to delete admin')
    elif await role_crud.get_user_role(role_id=role_id): # role_id参数可以为None，所以这里不能将role_id=role_id省略成role_id
        raise  HTTPException(status_code=400, detail='该角色已被用户绑定，请先解绑')
    if await role_crud.delete_role(role_id):
        return {"code": 201, "message": "success"}
    else:
        raise HTTPException(status_code=500, detail='Delete failed')
