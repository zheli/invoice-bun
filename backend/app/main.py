from fastapi import FastAPI
from app.api import auth, users, invoices
from app.db import init_db

app = FastAPI(title="Invoice Management API")

@app.on_event("startup")
async def on_startup():
    await init_db()

app.include_router(auth.router, prefix="", tags=["auth"])
app.include_router(users.router, prefix="", tags=["users"])
app.include_router(invoices.router, prefix="", tags=["invoices"])

@app.get("/")
async def root():
    return {"message": "Welcome to Invoice Management API"}
