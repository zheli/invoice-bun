import pytest
from httpx import AsyncClient
from app.models import User
from sqlmodel import select
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.mark.asyncio
async def test_google_login_redirect(client: AsyncClient):
    response = await client.get("/auth/google/login")
    assert response.status_code == 302
    assert "accounts.google.com" in response.headers["location"]


@pytest.mark.asyncio
async def test_google_callback_new_user(client: AsyncClient, session: AsyncSession):
    # Cleanup
    _ = await session.execute(
        text(
            "DELETE FROM invoice WHERE user_id IN (SELECT id FROM \"user\" WHERE email = 'test@example.com')"
        )
    )
    _ = await session.execute(
        text("DELETE FROM \"user\" WHERE email = 'test@example.com'")
    )
    await session.commit()

    # The google_sso is mocked in conftest.py to return a test user
    response = await client.get("/auth/google/callback")

    assert response.status_code == 307  # Redirects to frontend
    assert "token=" in response.headers["location"]

    # Verify user was created
    result = await session.execute(select(User).where(User.email == "test@example.com"))
    user = result.scalars().first()
    assert user is not None
    assert user.email == "test@example.com"
    assert user.provider == "google"
    assert user.provider_id == "123456789"


@pytest.mark.asyncio
async def test_google_callback_existing_user(
    client: AsyncClient, session: AsyncSession
):
    # Cleanup
    _ = await session.execute(
        text(
            "DELETE FROM invoice WHERE user_id IN (SELECT id FROM \"user\" WHERE email = 'test@example.com')"
        )
    )
    _ = await session.execute(
        text("DELETE FROM \"user\" WHERE email = 'test@example.com'")
    )
    await session.commit()

    # Create user first
    user = User(
        email="test@example.com",
        full_name="Test User",  # Changed from display_name to full_name to match model
        hashed_password="somepassword",
        provider="google",
        provider_id="123456789",
    )
    session.add(user)
    await session.commit()

    # Login again
    response = await client.get("/auth/google/callback")

    assert response.status_code == 307
    assert "token=" in response.headers["location"]

    # Verify we didn't create a duplicate
    result = await session.execute(select(User).where(User.email == "test@example.com"))
    users = result.scalars().all()
    assert len(users) == 1
