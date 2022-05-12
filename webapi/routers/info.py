from fastapi import APIRouter, Request
from ..common.log import logger


router = APIRouter(
    prefix= "/getinfo",
    tags= ["getinfo"],
    responses={404: {"description": "Not found"}}
)


@router.post("/")
async def get_info(*, request: Request):
    res = {
        "host": request.client.host,
        "port": request.client.port,
        "method": request.method,
        "url": request.url,
        "headers": request.headers,
        "cookies": request.cookies,
        "body": request.body
    }
    logger.info(str(res))
    return res