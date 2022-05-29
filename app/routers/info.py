from fastapi import APIRouter, Request
from ..utils.log_settings import logger
from ..utils.common import Common


router = APIRouter(
    prefix= "/info",
    tags= ["getinfo"],
    responses={404: {"description": "Not found"}}
)


# 获取请求数据，记录日志
@router.get("/")
async def get_info(*, request: Request):
    res = Common.get_request_info(request)
    logger.info(str(res))
    return res


# 获取请求数据，记录日志
@router.post("/")
async def get_info(*, request: Request):
    res = Common.get_request_info(request)
    res.update({"body": await request.json()})
    logger.info(str(res))
    return res