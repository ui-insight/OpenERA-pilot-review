"""Pydantic schemas for the pilot review dashboard."""

from __future__ import annotations

import datetime

from pydantic import BaseModel


# ---------------------------------------------------------------------------
# Entity read schemas
# ---------------------------------------------------------------------------

class OrganizationRead(BaseModel):
    organization_id: str
    organization_name: str | None = None
    organization_type: str | None = None
    source_system: str | None = None
    needs_lookup: bool = False
    model_config = {"from_attributes": True}


class PersonnelRead(BaseModel):
    personnel_id: str
    full_name: str | None = None
    last_name: str | None = None
    first_name: str | None = None
    person_type: str | None = None
    department_organization_id: str | None = None
    needs_identity_review: bool = False
    model_config = {"from_attributes": True}


class ProjectRead(BaseModel):
    project_id: str
    project_title: str | None = None
    project_status: str | None = None
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    needs_veras_title: bool = False
    model_config = {"from_attributes": True}


class ProposalRead(BaseModel):
    proposal_id: str
    proposal_number: str | None = None
    proposal_title: str | None = None
    project_id: str | None = None
    sponsor_organization_id: str | None = None
    proposal_status: str | None = None
    start_date: datetime.date | None = None
    end_date: datetime.date | None = None
    needs_veras_enrichment: bool = False
    title_source_type: str | None = None
    model_config = {"from_attributes": True}


class AwardRead(BaseModel):
    award_id: str
    award_number: str | None = None
    award_title: str | None = None
    proposal_id: str | None = None
    project_id: str | None = None
    sponsor_organization_id: str | None = None
    award_status: str | None = None
    original_start_date: datetime.date | None = None
    current_end_date: datetime.date | None = None
    adjusted_budget: float | None = None
    cumulative_funding_amount: float | None = None
    needs_veras_title: bool = False
    title_source_type: str | None = None
    model_config = {"from_attributes": True}


class DocumentRead(BaseModel):
    document_id: str
    document_type_code: str | None = None
    document_type_label: str | None = None
    parent_entity_type: str | None = None
    parent_entity_id: str | None = None
    linked_proposal_id: str | None = None
    top_level_bucket: str | None = None
    filename: str | None = None
    extension: str | None = None
    mime_type: str | None = None
    file_size_bytes: int | None = None
    storage_relative_path: str | None = None
    is_content_duplicate: bool = False
    needs_review: str | None = None
    model_config = {"from_attributes": True}


class ProjectRoleRead(BaseModel):
    project_role_id: str
    project_id: str | None = None
    personnel_id: str | None = None
    role_code: str | None = None
    key_personnel: bool = False
    funding_award_id: str | None = None
    model_config = {"from_attributes": True}


class AllowedValueRead(BaseModel):
    allowed_value_id: str
    group_name: str | None = None
    code: str | None = None
    label: str | None = None
    description: str | None = None
    model_config = {"from_attributes": True}


# ---------------------------------------------------------------------------
# Aggregated pilot dashboard schemas
# ---------------------------------------------------------------------------

class PilotRecordSummary(BaseModel):
    """Summary card for one pilot record on the dashboard."""
    record_id: str
    description: str
    title: str | None = None
    award_count: int = 0
    proposal_count: int = 0
    document_count: int = 0
    duplicate_count: int = 0
    total_budget: float = 0.0
    has_title_gaps: bool = False
    has_award: bool = True


class PilotDashboard(BaseModel):
    """Top-level dashboard response."""
    records: list[PilotRecordSummary]
    total_awards: int = 0
    total_proposals: int = 0
    total_documents: int = 0
    total_duplicates: int = 0
    total_budget: float = 0.0


class PilotRecordDetail(BaseModel):
    """Full detail view for a single pilot record."""
    record_id: str
    description: str
    awards: list[AwardRead] = []
    proposals: list[ProposalRead] = []
    projects: list[ProjectRead] = []
    documents: list[DocumentRead] = []
    personnel: list[PersonnelRead] = []
    document_count: int = 0
    duplicate_count: int = 0
    category_counts: dict[str, int] = {}


class DocumentFilterResult(BaseModel):
    """Paginated document list with facets."""
    items: list[DocumentRead]
    total_count: int
    page: int
    page_size: int
    category_counts: dict[str, int] = {}
