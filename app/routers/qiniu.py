from fastapi import APIRouter, Depends, HTTPException, UploadFile, Request
from sqlalchemy.orm import Session
from ..db import crud, schemas
from ..db.database import get_db
from ..utils.common import Common
from ..utils.config import get_qiniu_config
from ..utils.qiniu_upload import qiniu_upload_token
from ..utils.log_settings import logger


router = APIRouter(
    prefix="/qiniu",
    tags=["七牛云存储"],
    responses={404: {"description": "Not found"}}
)


@router.get("/files", response_model=schemas.Files, summary='文件列表')
async def read_files(db: Session=Depends(get_db)):
    return {"code": 20000, "data": crud.get_files(db=db)}


@router.post("/callback", summary='七牛回调')
async def qiniu_callback(data: schemas.FileCreate, db: Session=Depends(get_db)):
    crud.create_file(db=db, url= get_qiniu_config()['external_link_base'] + '/' + data.key)
    return {"code": 20000, "data": dict({"key": data.key})}


@router.get("/upload/token", summary='获取七牛token')
async def get_upload_token():
    return {"code": 20000, "data": dict({"token": qiniu_upload_token()})}