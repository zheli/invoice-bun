import uuid
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.db import get_session
from app.models import Invoice, InvoiceCreate, InvoiceUpdate, User
from app.api import deps
from app.services.pdf_service import generate_pdf

router = APIRouter()

@router.get("/invoices/", response_model=List[Invoice])
async def read_invoices(
    session: AsyncSession = Depends(get_session),
    current_user: User = Depends(deps.get_current_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    query = select(Invoice).where(Invoice.user_id == current_user.id).offset(skip).limit(limit)
    result = await session.execute(query)
    return result.scalars().all()

@router.post("/invoices/", response_model=Invoice)
async def create_invoice(
    *,
    session: AsyncSession = Depends(get_session),
    invoice_in: InvoiceCreate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    invoice = Invoice(**invoice_in.dict(), user_id=current_user.id)
    session.add(invoice)
    await session.commit()
    await session.refresh(invoice)
    return invoice

@router.get("/invoices/{invoice_id}", response_model=Invoice)
async def read_invoice(
    *,
    session: AsyncSession = Depends(get_session),
    invoice_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    result = await session.execute(select(Invoice).where(Invoice.id == invoice_id, Invoice.user_id == current_user.id))
    invoice = result.scalars().first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")
    return invoice

@router.put("/invoices/{invoice_id}", response_model=Invoice)
async def update_invoice(
    *,
    session: AsyncSession = Depends(get_session),
    invoice_id: uuid.UUID,
    invoice_in: InvoiceUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    result = await session.execute(select(Invoice).where(Invoice.id == invoice_id, Invoice.user_id == current_user.id))
    invoice = result.scalars().first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    invoice_data = invoice_in.dict(exclude_unset=True)
    for key, value in invoice_data.items():
        setattr(invoice, key, value)

    session.add(invoice)
    await session.commit()
    await session.refresh(invoice)
    return invoice

@router.delete("/invoices/{invoice_id}", response_model=Invoice)
async def delete_invoice(
    *,
    session: AsyncSession = Depends(get_session),
    invoice_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    result = await session.execute(select(Invoice).where(Invoice.id == invoice_id, Invoice.user_id == current_user.id))
    invoice = result.scalars().first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    await session.delete(invoice)
    await session.commit()
    return invoice

@router.get("/invoices/{invoice_id}/pdf")
async def get_invoice_pdf(
    *,
    session: AsyncSession = Depends(get_session),
    invoice_id: uuid.UUID,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    result = await session.execute(select(Invoice).where(Invoice.id == invoice_id, Invoice.user_id == current_user.id))
    invoice = result.scalars().first()
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found")

    pdf_content = generate_pdf(invoice, current_user)
    return Response(content=pdf_content, media_type="application/pdf")
