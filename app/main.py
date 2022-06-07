from fastapi import Depends, FastAPI
from .dependencies import get_token_header
from .internal import login, logout
from .routers import items, users, info
from .db import models
from .db.database import engine
from .utils.config import GetConfig


api_route_depends = GetConfig.get_api_route_depends()

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="lrtest",
    version="1.0.0",
    description="lrtest",
    openapi_url="{depends}/openapi.json".format(depends=api_route_depends),
    docs_url="{depends}/docs".format(depends=api_route_depends)
)

app.include_router(login.router, prefix=api_route_depends)
app.include_router(users.router, prefix=api_route_depends)
app.include_router(items.router, prefix=api_route_depends, dependencies=[Depends(get_token_header)])
app.include_router(info.router, prefix=api_route_depends, dependencies=[Depends(get_token_header)])
app.include_router(logout.router, prefix=api_route_depends)


@app.get(api_route_depends)
async def root():
    return {"message": "test1 Hello Bigger Applications!"}
