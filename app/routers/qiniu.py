import re
from fastapi import APIRouter
from ..utils.config import get_qiniu_config
from ..crud import qiniu_crud


router = APIRouter(
    prefix="/qiniu",
    tags=["七牛云存储"]
)


@router.get("/files", summary='获取七牛文件列表')
async def read_qiniu_files():
    # url前缀
    url_base = get_qiniu_config()['external_link_base']
    # 七牛文件列表
    file_list = dict(qiniu_crud.get_qiniu_list()[0])['items']
    # 列表按照上传时间降序排列
    file_list = sorted(file_list, key= lambda item: item['putTime'])
    file_list.reverse()
    # 只提取列表信息中的url
    url_list = list(map(lambda item: url_base + '/' + item['key'], file_list))
    return {"code": 20000, "message": "success", "data": url_list}


@router.delete("/files", summary='批量删除文件')
async def delete_qiniu_files(body: list):
    a = '12346/hhhhhhhhcom/asdf'
    b = re.search(r'/.*\b', a).group()
    # keys = list(map(lambda item: re.search(r'/.*', item).group(), body))
    return {"out": b}


@router.post("/callback", summary='七牛回调')
async def qiniu_callback(body: dict):
    return {"code": 20000, "message": "success", "data": dict({"key": body['key']})}


@router.get("/upload/token", summary='获取七牛token')
async def get_qiniu_upload_token():
    return {"code": 20000, "message": "success", "data": dict({"token": qiniu_crud.get_qiniu_upload_token()})}
