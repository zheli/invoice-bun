import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Invoice Management API"
    DATABASE_URL: str
    SECRET_KEY: str = "your-secret-key-here"  # TODO: Change this in production
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    PORT: int = 8000
    GOOGLE_CLIENT_ID: str = "your-google-client-id"
    GOOGLE_CLIENT_SECRET: str = "your-google-client-secret"
    GOOGLE_REDIRECT_URI: str = (
        f"http://localhost:{os.getenv('PORT', '8000')}/auth/google/callback"
    )

    class Config:
        case_sensitive: bool = True
        env_file: str = ".env"


settings = Settings()  # pyright: ignore[reportCallIssue]
