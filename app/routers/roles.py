from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database.mysql import get_db
from ..crud import role_crud
from ..schemas import role_schemas
from ..permission import role_depends


router = APIRouter(
    prefix="/roles",
    tags=["角色"]
)


@router.get("", response_model=role_schemas.RoleResponse, summary='查询角色', dependencies=[Depends(role_depends())])
async def get_users(db_session: Session=Depends(get_db)):
    return {"code": 20000, "message": "success", "data": role_crud.get_roles(db_session)}
