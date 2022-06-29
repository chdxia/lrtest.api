from fastapi import APIRouter, Body
from ..utils.config import get_qiniu_config
from ..utils.qiniu import qiniu_upload_token
from ..utils.qiniu import get_qiniu_list


router = APIRouter(
    prefix="/qiniu",
    tags=["七牛云存储"]
)


@router.get("/files", summary='获取七牛文件列表')
async def read_qiniu_files():
    # url前缀
    url_base = get_qiniu_config()['external_link_base']
    # 七牛文件列表
    file_list = dict(get_qiniu_list()[0])['items']
    # 只提取列表信息中的url
    url_list = list(map(lambda item: url_base + '/' + item['key'], file_list))
    return {"code": 20000, "message": "success", "data": url_list}


@router.post("/callback", summary='七牛回调')
async def qiniu_callback(body: dict):
    return {"code": 20000, "message": "success", "data": dict({"key": body['key']})}


@router.get("/upload/token", summary='获取七牛token')
async def get_qiniu_upload_token():
    return {"code": 20000, "message": "success", "data": dict({"token": qiniu_upload_token()})}
