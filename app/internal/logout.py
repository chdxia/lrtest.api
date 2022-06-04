from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..db import crud, models, schemas
from ..db.database import get_db
from ..utils.common import Common


router = APIRouter(
    prefix="/logout",
    tags=["login"],
)

@router.post("")
async def logout():
    return {
        "code": 20000,
        "data": 'success'
      }