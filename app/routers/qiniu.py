from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..db import crud, schemas
from ..db.database import get_db
from ..utils.config import get_qiniu_config
from ..utils.qiniu_upload import qiniu_upload_token


router = APIRouter(
    prefix="/qiniu",
    tags=["七牛云存储"]
)


@router.get("/files", response_model=schemas.FilesResponse, summary='文件列表')
async def read_files(db_session: Session=Depends(get_db)):
    return {"code": 20000, "message": "success", "data": list(map(lambda item: item.url, crud.get_files(db_session)))}


@router.post("/callback", summary='七牛回调')
async def qiniu_callback(data: schemas.FileCreate, db_session: Session=Depends(get_db)):
    crud.create_file(db_session, url= get_qiniu_config()['external_link_base'] + '/' + data.key)
    return {"code": 20000, "message": "success", "data": dict({"key": data.key})}


@router.get("/upload/token", summary='获取七牛token')
async def get_upload_token():
    return {"code": 20000, "message": "success", "data": dict({"token": qiniu_upload_token()})}
