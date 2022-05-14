from fastapi import APIRouter, Request
from ..utils.log_settings import logger
from ..utils.get_info import get_request_info


router = APIRouter(
    prefix= "/info",
    tags= ["getinfo"],
    responses={404: {"description": "Not found"}}
)


@router.post("/")
async def get_info(*, request: Request):
    res = get_request_info(request)
    res.update({"body": await request.json()})
    logger.info(str(res))
    return res