from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from .middleware import Events, Exception, Middleware
from .lib import get_api_route_depends
from .api import login, users, qiniu, roles


app = FastAPI(
    title='lrtest',
    version='1.0.0',
    description='this is lrtest swagger docs',
    openapi_url=f'{get_api_route_depends()}/openapi.json',
    docs_url=f'{get_api_route_depends()}/docs',
    responses={404: {"code": 40000, "message": "not found"}}
)


# 事件监听
app.add_event_handler("startup", Events.startup(app))
app.add_event_handler("shutdown", Events.shutdown(app))


# 异常处理
app.add_exception_handler(HTTPException, Exception.http_error_handler)
app.add_exception_handler(RequestValidationError, Exception.http422_error_handler)
app.add_exception_handler(Exception.UnicornException, Exception.unicorn_exception_handler)


# 注册中间件
app.add_middleware(Middleware.LogerMiddleware)


# 路由
app.include_router(login.router, prefix=get_api_route_depends())
app.include_router(users.router, prefix=get_api_route_depends())
app.include_router(roles.router, prefix=get_api_route_depends())
app.include_router(qiniu.router, prefix=get_api_route_depends())
