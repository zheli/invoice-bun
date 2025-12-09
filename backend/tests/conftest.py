import pytest
from fastapi.responses import RedirectResponse
from collections.abc import AsyncGenerator
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from app.main import app
from app.db import get_session
from app.core.config import settings

# Use an in-memory SQLite database for testing or a separate test DB
# For now, let's use the same DB but rollback transactions, or better, use SQLite for isolation if possible.
# However, the app uses asyncpg which is Postgres specific.
# So we must use Postgres. We can rely on the existing DB for now but use transaction rollback.
# CAUTION: This might affect local DB if not careful. Ideally we should create a test DB.
# Given the constraints and existing env, I will try to use the existing DB but wrap in transaction.

from sqlalchemy.pool import NullPool

# Override dependency
engine = create_async_engine(
    settings.DATABASE_URL, echo=False, future=True, poolclass=NullPool
)
TestingSessionLocal = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


@pytest.fixture
async def session() -> AsyncGenerator[AsyncSession, None]:
    async with TestingSessionLocal() as session:
        yield session


@pytest.fixture
async def client(session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    # Override get_session dependency
    async def override_get_session():
        yield session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c

    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def mock_google_sso(monkeypatch: pytest.MonkeyPatch):
    class MockGoogleSSO:
        def __init__(self, **kwargs: object):  # pyright: ignore[reportUnusedParameter]
            pass

        async def __aenter__(self):
            return self

        async def __aexit__(self, exc_type: object, exc_val: object, exc_tb: object):
            pass

        async def get_login_redirect(self, **kwargs: object):  # pyright: ignore[reportUnusedParameter]
            return RedirectResponse(
                url="http://accounts.google.com/o/oauth2/auth", status_code=302
            )

        async def verify_and_process(self, request: object):  # pyright: ignore[reportUnusedParameter]
            class UserInfo:
                email: str
                display_name: str
                id: str
                picture: str

                def __init__(self):
                    self.email = "test@example.com"
                    self.display_name = "Test User"
                    self.id = "123456789"
                    self.picture = "http://example.com/pic.jpg"

            return UserInfo()

    monkeypatch.setattr("app.api.auth.GoogleSSO", MockGoogleSSO)
