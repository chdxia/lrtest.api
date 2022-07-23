from fastapi import FastAPI
from ..database.mysql import register_mysql


def startup(app: FastAPI):
    async def app_start():
        print("===fastapi started===")
        await register_mysql(app)
    return app_start


def shutdown(app: FastAPI):
    async def app_stop():
        print("===fastapi stopped===")
    return app_stop
