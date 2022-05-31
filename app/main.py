from fastapi import Depends, FastAPI
from .dependencies import get_query_token, get_token_header
from .internal import admin, login
from .routers import item, user, info
from .db import models
from .db.database import engine



models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    # dependencies=[Depends(get_query_token)],
    title="fastapi-demo",
    version="0.0.1",
    description="this is a demo"
)


app.include_router(user.router)
app.include_router(item.router)
app.include_router(info.router)
app.include_router(login.router)
app.include_router(
    admin.router,
    # prefix="/admin",
    # tags=["admin"],
    # dependencies=[Depends(get_token_header)],
    responses={418: {"description": "I'm a teapot"}}
)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
