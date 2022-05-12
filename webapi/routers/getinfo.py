from fastapi import APIRouter
from ..db import schemas


router = APIRouter(
    prefix= "/getinfo",
    tags= ["getinfo"],
    responses={404: {"description": "Not found"}}
)


@router.post("/{get_id}")
async def get_info(user: schemas.UserCreate,get_id: int, name: str | None = None):
    pass