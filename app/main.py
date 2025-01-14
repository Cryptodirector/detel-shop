from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.staticfiles import StaticFiles
from starlette import status
from starlette.middleware.cors import CORSMiddleware

from app.routers.categories import router
from app.security.auth import router as auth_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static"
)


app.include_router(router)
app.include_router(auth_router)
