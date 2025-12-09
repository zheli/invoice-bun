from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.core.config import settings
from app.models import User
from app.security import ALGORITHM
from sqlmodel import select

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/auth/access-token")


class TokenPayload(BaseModel):
    sub: str | None = None


async def get_current_user(
    session: AsyncSession = Depends(get_session),  # pyright: ignore[reportCallInDefaultInitializer]
    token: str = Depends(reusable_oauth2),  # pyright: ignore[reportCallInDefaultInitializer]
) -> User:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)  # pyright: ignore[reportAny]
    except (JWTError, Exception):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    result = await session.execute(select(User).where(User.id == token_data.sub))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
