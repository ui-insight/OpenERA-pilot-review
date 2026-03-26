"""Pilot review dashboard API endpoints."""

from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.allowed_value import AllowedValue
from app.schemas.pilot import (
    AllowedValueRead,
    DocumentFilterResult,
    PilotDashboard,
    PilotRecordDetail,
)
from app.services import pilot_service

router = APIRouter()


@router.get("/dashboard", response_model=PilotDashboard)
async def dashboard(db: AsyncSession = Depends(get_db)):
    """Overview of all 5 pilot records with summary stats."""
    return await pilot_service.get_dashboard(db)


@router.get("/records/{record_id}", response_model=PilotRecordDetail)
async def record_detail(record_id: str, db: AsyncSession = Depends(get_db)):
    """Full detail view for a single pilot record."""
    result = await pilot_service.get_record_detail(db, record_id)
    if result is None:
        raise HTTPException(status_code=404, detail=f"Pilot record '{record_id}' not found")
    return result


@router.get("/records/{record_id}/documents", response_model=DocumentFilterResult)
async def record_documents(
    record_id: str,
    category: str | None = Query(None),
    parent_type: str | None = Query(None),
    is_duplicate: bool | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Documents for a specific pilot record, with optional filters."""
    return await pilot_service.get_documents_filtered(
        db, record_id=record_id, category=category, parent_type=parent_type,
        is_duplicate=is_duplicate, search=search, page=page, page_size=page_size,
    )


@router.get("/documents", response_model=DocumentFilterResult)
async def all_documents(
    record_id: str | None = Query(None),
    category: str | None = Query(None),
    parent_type: str | None = Query(None),
    is_duplicate: bool | None = Query(None),
    search: str | None = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(25, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """All documents across pilot records, with optional filters."""
    return await pilot_service.get_documents_filtered(
        db, record_id=record_id, category=category, parent_type=parent_type,
        is_duplicate=is_duplicate, search=search, page=page, page_size=page_size,
    )


@router.get("/allowed-values/document-types", response_model=list[AllowedValueRead])
async def document_types(db: AsyncSession = Depends(get_db)):
    """Reference list of document type categories."""
    result = await db.execute(
        select(AllowedValue)
        .where(AllowedValue.group_name == "Document_Type")
        .order_by(AllowedValue.label)
    )
    return [AllowedValueRead.model_validate(av) for av in result.scalars().all()]
