# pyright: reportUnknownVariableType=false
from typing import Any
from sqlalchemy import JSON, Column
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime, timezone
import uuid


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: str | None = None
    company_name: str | None = None
    hashed_password: str

    # Social Auth
    provider: str | None = None
    provider_id: str | None = None
    is_active: bool = True
    is_superuser: bool = False


class User(UserBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    invoices: list["Invoice"] = Relationship(back_populates="user")  # pyright: ignore[reportAny]


class Token(SQLModel):
    access_token: str
    token_type: str


class UserCreate(SQLModel):
    email: str
    password: str
    full_name: str | None = None
    company_name: str | None = None


class InvoiceBase(SQLModel):
    invoice_number: str
    date: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    due_date: datetime | None = None
    client_name: str
    client_email: str | None = None
    total_amount: float = 0.0
    status: str = "draft"  # draft, sent, paid
    content: dict[str, Any] = Field(  # pyright: ignore[reportExplicitAny]
        default={}, sa_column=Column(JSON)
    )  # Stores full invoice data/items


class Invoice(InvoiceBase, table=True):
    id: uuid.UUID | None = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="invoices")  # pyright: ignore[reportAny]


class InvoiceCreate(InvoiceBase):
    pass


class InvoiceUpdate(SQLModel):
    invoice_number: str | None = None
    date: datetime | None = None
    due_date: datetime | None = None
    client_name: str | None = None
    client_email: str | None = None
    total_amount: float | None = None
    status: str | None = None
    content: dict[str, Any] | None = None  # pyright: ignore[reportExplicitAny]
