from fastapi import Depends, FastAPI, Request
from .dependencies import get_token_header
from .internal import login
from .routers import items, users
from .db import models
from .db.database import engine
from .utils.config import GetConfig
from .utils.log_settings import logger
from .utils.common import Common


api_route_depends = GetConfig.get_api_route_depends()


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="lrtest",
    version="1.0.0",
    description="this is lrtest swagger docs",
    openapi_url="{depends}/openapi.json".format(depends=api_route_depends),
    docs_url="{depends}/docs".format(depends=api_route_depends)
)


@app.post(api_route_depends, responses={404: {"description": "Not found"}}, tags=["hello_word"], summary='返回请求信息')
async def return_info(*, request: Request):
    req = Common.get_request_info(request)
    req.update({"body": await request.json()})
    logger.info(str(req))
    return req


app.include_router(login.router, prefix=api_route_depends)
app.include_router(users.router, prefix=api_route_depends, dependencies=[Depends(get_token_header)])
app.include_router(items.router, prefix=api_route_depends, dependencies=[Depends(get_token_header)])