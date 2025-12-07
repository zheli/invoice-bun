from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.models import User
from app.api import deps
from app.security import get_password_hash

router = APIRouter()

@router.post("/users/", response_model=User)
async def create_user(
    *,
    session: AsyncSession = Depends(get_session),
    user_in: User,
) -> Any:
    result = await session.execute(select(User).where(User.email == user_in.email))
    user = result.scalars().first()
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    
    user_in.hashed_password = get_password_hash(user_in.hashed_password)
    session.add(user_in)
    await session.commit()
    await session.refresh(user_in)
    return user_in

@router.get("/users/me", response_model=User)
async def read_user_me(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    return current_user
