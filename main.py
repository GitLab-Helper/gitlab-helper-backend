import os

from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

from routers import auth, groups

app = FastAPI(root_path="/api", version="0.2.1")

origins = [os.getenv("URL", "*")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    auth.router,
    prefix="/auth",
)
app.include_router(
    groups.router,
    prefix="/groups",
    tags=["groups"],
)


@app.get("/")
async def read_root_path():
    raise HTTPException(
        status_code=418,
        detail="I'm a teapot",
        headers={"X-Error": "I'm a teapot"},
    )
