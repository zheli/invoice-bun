from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from app.db import get_session
from app.api import deps
from app.core.config import settings
from app.security import create_access_token, verify_password
from app.models import User, Token, UserCreate
from fastapi_sso.sso.google import GoogleSSO
from app.security import get_password_hash
import uuid

router = APIRouter()

google_sso = GoogleSSO(
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    redirect_uri=settings.GOOGLE_REDIRECT_URI,
    allow_insecure_http=True, # For local dev
)

@router.post("/auth/access-token", response_model=Token)
async def login_access_token(
    session: AsyncSession = Depends(get_session), 
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    result = await session.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }

@router.get("/auth/google/login")
async def google_login():
    return await google_sso.get_login_redirect()

@router.get("/auth/google/callback")
async def google_callback(request: Request, session: AsyncSession = Depends(get_session)):
    try:
        user_info = await google_sso.verify_and_process(request)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    if not user_info.email:
        raise HTTPException(status_code=400, detail="No email returned from Google")

    # Check if user exists
    user_result = await session.execute(select(User).where(User.email == user_info.email))
    user = user_result.scalars().first()

    if not user:
        # Register new user
        password = str(uuid.uuid4()) # Random password
        user = User(
            email=user_info.email,
            full_name=user_info.display_name,
            hashed_password=get_password_hash(password),
            provider="google",
            provider_id=user_info.id,
            is_active=True
        )
        session.add(user)
        await session.commit()
        await session.refresh(user)
    else:
        # Link if not linked? Or just login. 
        # Ideally we should check if provider matches or handle merging.
        # For now, just logging in is fine as email is trusted.
        pass

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    token = create_access_token(user.id, expires_delta=access_token_expires)
    
    # Redirect to frontend with token
    # Assuming frontend is on 5173
    return RedirectResponse(url=f"http://localhost:5173/auth/callback?token={token}")
