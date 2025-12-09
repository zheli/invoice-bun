from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import auth, users, invoices
from app.db import init_db

from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(_app: FastAPI):
    await init_db()
    yield


app = FastAPI(title="Invoice Management API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(users.router, prefix="", tags=["users"])
app.include_router(invoices.router, prefix="", tags=["invoices"])


@app.get("/")
async def root():
    return {"message": "Welcome to Invoice Management API"}
