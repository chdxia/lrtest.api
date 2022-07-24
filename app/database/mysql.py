from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise
from ..lib import get_mysql_credentials
from ..models import model


DB_ORM_CONFIG = {
    'connections': {
        'default': {
            'engine': 'tortoise.backends.mysql',
            'credentials': get_mysql_credentials()}
    },
    'apps': {
        'models': {'models': [model], 'default_connection': 'default'}
    },
    'use_tz': False,
    'timezone': 'Asia/Shanghai'
}


async def register_mysql(app: FastAPI):
    register_tortoise(
        app,
        config=DB_ORM_CONFIG,
        generate_schemas=False, #立即生成models对应的表，建议只在dev设置为True
        add_exception_handlers=True,
    )
