from fastapi import FastAPI
from ..database.mysql import register_mysql
from ..utils.scheduler import register_scheduler


def startup(app: FastAPI):
    async def app_start():
        await register_mysql(app) # 注册数据库，挂载到app
        await register_scheduler(app) # 注册定时器，挂载到app
        print("===fastapi started===")
    return app_start


def shutdown(app: FastAPI):
    async def app_stop():
        print("===fastapi stopped===")
    return app_stop
