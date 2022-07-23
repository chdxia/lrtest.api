from ..lib import get_mysql_credentials
from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise


DB_ORM_CONFIG = {
    'connections': {
        'base': {'engine': 'tortoise.backends.mysql', 'credentials': get_mysql_credentials()}
    },
    'apps': {
        'base': {'models': ['models.base'], 'default_connection': 'base'}
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}


async def register_mysql(app: FastAPI):
    register_tortoise(
        app,
        config=DB_ORM_CONFIG,
        generate_schemas=False,
        add_exception_handlers=True,
    )
