from fastapi import FastAPI, HTTPException, Request
from fastapi.exceptions import RequestValidationError
from .database.mysql import engine
from .models import models
from .lib import Exception, Middleware, logger, get_api_route_depends, get_request_info
from .api import login, users, qiniu, roles


models.Base.metadata.create_all(bind=engine)


app = FastAPI(
    title='lrtest',
    version='1.0.0',
    description='this is lrtest swagger docs',
    openapi_url=f'{get_api_route_depends()}/openapi.json',
    docs_url=f'{get_api_route_depends()}/docs',
    responses={404: {"code": 40000, "message": "not found"}}
)


# 异常处理
app.add_exception_handler(HTTPException, Exception.http_error_handler)
app.add_exception_handler(RequestValidationError, Exception.http422_error_handler)
app.add_exception_handler(Exception.UnicornException, Exception.unicorn_exception_handler)


# 注册中间件
app.add_middleware(Middleware.LogerMiddleware)


# hello_word
@app.post(get_api_route_depends(), tags=["hello_word"], summary='返回请求信息')
async def return_info(*, request: Request):
    req = get_request_info(request)
    req.update({"body": await request.json()})
    logger.info(str(req))
    return req

# 路由
app.include_router(login.router, prefix=get_api_route_depends())
app.include_router(users.router, prefix=get_api_route_depends())
app.include_router(roles.router, prefix=get_api_route_depends())
app.include_router(qiniu.router, prefix=get_api_route_depends())
