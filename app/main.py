from fastapi import Depends, FastAPI
from .dependencies import get_token_header
from .internal import admin, login
from .routers import items, users, info
from .db import models
from .db.database import engine



models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="lrtest",
    version="1.0.0",
    description="lrtest"
)


app.include_router(users.router, dependencies=[Depends(get_token_header)])
app.include_router(items.router, dependencies=[Depends(get_token_header)])
app.include_router(info.router, dependencies=[Depends(get_token_header)])
app.include_router(login.router)
app.include_router(admin.router)


@app.get("/")
async def root():
    return {"message": "Hello Bigger Applications!"}
