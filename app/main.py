import time
from fastapi import Depends, FastAPI, Request
from .dependencies import get_token_header
from .internal import login
from .routers import items, users, qiniu
from .db import models
from .db.database import engine
from .utils.config import get_api_route_depends
from .utils.log_settings import logger
from .utils.common import get_request_info


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title='lrtest',
    version='1.0.0',
    description='this is lrtest swagger docs',
    openapi_url=f'{get_api_route_depends()}/openapi.json',
    docs_url=f'{get_api_route_depends()}/docs',
    responses={404: {"code": 40000, "message": "not found"}}
)


@app.middleware('http')
async def log_requests(request, call_next):
    '''中间件，记录请求日志'''
    start_time = time.time()

    response = await call_next(request)

    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f'{request.method} {request.url} completed_in={formatted_process_time}ms status_code={response.status_code}')
    return response


@app.post(get_api_route_depends(), tags=["hello_word"], summary='返回请求信息')
async def return_info(*, request: Request):
    req = get_request_info(request)
    req.update({"body": await request.json()})
    logger.info(str(req))
    return req


app.include_router(login.router, prefix=get_api_route_depends())
app.include_router(users.router, prefix=get_api_route_depends(), dependencies=[Depends(get_token_header)])
app.include_router(items.router, prefix=get_api_route_depends(), dependencies=[Depends(get_token_header)])
app.include_router(qiniu.router, prefix=get_api_route_depends())
