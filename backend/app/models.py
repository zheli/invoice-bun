from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship
from datetime import datetime
import uuid

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: Optional[str] = None
    company_name: Optional[str] = None
    hashed_password: str
    
    # Social Auth
    provider: Optional[str] = None
    provider_id: Optional[str] = None
    is_active: bool = True
    is_superuser: bool = False

class User(UserBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    invoices: List["Invoice"] = Relationship(back_populates="user")

from sqlalchemy import JSON, Column

class InvoiceBase(SQLModel):
    invoice_number: str
    date: datetime = Field(default_factory=datetime.utcnow)
    due_date: Optional[datetime] = None
    client_name: str
    client_email: Optional[str] = None
    total_amount: float = 0.0
    status: str = "draft" # draft, sent, paid
    content: dict = Field(default={}, sa_column=Column(JSON)) # Stores full invoice data/items

class Invoice(InvoiceBase, table=True):
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")
    user: User = Relationship(back_populates="invoices")

class InvoiceCreate(InvoiceBase):
    pass

class InvoiceUpdate(SQLModel):
    invoice_number: Optional[str] = None
    date: Optional[datetime] = None
    due_date: Optional[datetime] = None
    client_name: Optional[str] = None
    client_email: Optional[str] = None
    total_amount: Optional[float] = None
    status: Optional[str] = None
    content: Optional[dict] = None
