"""Business logic for the pilot review dashboard."""

from __future__ import annotations

from collections import defaultdict

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.award import Award
from app.models.document import Document
from app.models.personnel import Personnel
from app.models.project import Project
from app.models.project_role import ProjectRole
from app.models.proposal import Proposal
from app.schemas.pilot import (
    AwardRead,
    DocumentFilterResult,
    DocumentRead,
    PersonnelRead,
    PilotDashboard,
    PilotRecordDetail,
    PilotRecordSummary,
    ProjectRead,
    ProposalRead,
)

# Pilot record configuration
PILOT_RECORDS: dict[str, dict] = {
    "AA4673": {
        "award_ids": ["AA4673"],
        "description": "Active award with amendments and prior approvals",
    },
    "AA6006": {
        "award_ids": ["AA6006"],
        "description": "Award with subawards and linked submissions",
    },
    "OS7090": {
        "award_ids": ["OS7090"],
        "description": "Largest local corpus in the current workspace",
    },
    "SI3394": {
        "award_ids": ["SI3394"],
        "description": "Mixed legacy and modern proposal identifiers",
    },
    "V250261": {
        "award_ids": [],
        "description": "Recent proposal-focused record (no award)",
    },
}


async def get_dashboard(db: AsyncSession) -> PilotDashboard:
    """Build the pilot dashboard with summary stats for each record."""
    records: list[PilotRecordSummary] = []
    totals = {"awards": 0, "proposals": 0, "documents": 0, "duplicates": 0, "budget": 0.0}

    for record_id, config in PILOT_RECORDS.items():
        # Awards for this record
        award_ids = config["award_ids"]
        award_count = 0
        proposal_ids: set[str] = set()
        total_budget = 0.0
        title: str | None = None
        has_title_gaps = False

        if award_ids:
            result = await db.execute(
                select(Award).where(Award.award_id.in_(award_ids))
            )
            awards = result.scalars().all()
            award_count = len(awards)
            for a in awards:
                if a.proposal_id:
                    proposal_ids.add(a.proposal_id)
                total_budget += a.cumulative_funding_amount or 0
                if a.award_title:
                    title = a.award_title
                if a.needs_veras_title:
                    has_title_gaps = True

        # If no title from award, try proposals
        if not title and proposal_ids:
            result = await db.execute(
                select(Proposal).where(Proposal.proposal_id.in_(proposal_ids))
            )
            for p in result.scalars().all():
                if p.proposal_title:
                    title = p.proposal_title
                    break

        # For proposal-only records, count proposals from documents
        if not award_ids:
            result = await db.execute(
                select(Document.linked_proposal_id)
                .where(Document.top_level_bucket == record_id)
                .distinct()
            )
            proposal_ids = {r[0] for r in result.all() if r[0]}
            # Try to get title from proposal
            if proposal_ids:
                result = await db.execute(
                    select(Proposal).where(Proposal.proposal_id.in_(proposal_ids))
                )
                for p in result.scalars().all():
                    if p.proposal_title:
                        title = p.proposal_title
                        break

        # Documents for this bucket
        result = await db.execute(
            select(func.count()).where(Document.top_level_bucket == record_id)
        )
        doc_count = result.scalar() or 0

        result = await db.execute(
            select(func.count()).where(
                Document.top_level_bucket == record_id,
                Document.is_content_duplicate == True,  # noqa: E712
            )
        )
        dup_count = result.scalar() or 0

        records.append(PilotRecordSummary(
            record_id=record_id,
            description=config["description"],
            title=title,
            award_count=award_count,
            proposal_count=len(proposal_ids),
            document_count=doc_count,
            duplicate_count=dup_count,
            total_budget=total_budget,
            has_title_gaps=has_title_gaps,
            has_award=bool(award_ids),
        ))

        totals["awards"] += award_count
        totals["proposals"] += len(proposal_ids)
        totals["documents"] += doc_count
        totals["duplicates"] += dup_count
        totals["budget"] += total_budget

    return PilotDashboard(
        records=records,
        total_awards=totals["awards"],
        total_proposals=totals["proposals"],
        total_documents=totals["documents"],
        total_duplicates=totals["duplicates"],
        total_budget=totals["budget"],
    )


async def get_record_detail(db: AsyncSession, record_id: str) -> PilotRecordDetail | None:
    """Build the full detail view for a single pilot record."""
    config = PILOT_RECORDS.get(record_id)
    if not config:
        return None

    award_ids = config["award_ids"]
    awards: list[AwardRead] = []
    proposal_ids: set[str] = set()
    project_ids: set[str] = set()

    # Awards
    if award_ids:
        result = await db.execute(select(Award).where(Award.award_id.in_(award_ids)))
        for a in result.scalars().all():
            awards.append(AwardRead.model_validate(a))
            if a.proposal_id:
                proposal_ids.add(a.proposal_id)
            if a.project_id:
                project_ids.add(a.project_id)

    # Also gather proposal IDs from documents for this bucket
    result = await db.execute(
        select(Document.linked_proposal_id)
        .where(Document.top_level_bucket == record_id)
        .distinct()
    )
    for row in result.all():
        if row[0]:
            proposal_ids.add(row[0])

    # Proposals
    proposals: list[ProposalRead] = []
    if proposal_ids:
        result = await db.execute(
            select(Proposal).where(Proposal.proposal_id.in_(proposal_ids))
        )
        for p in result.scalars().all():
            proposals.append(ProposalRead.model_validate(p))
            if p.project_id:
                project_ids.add(p.project_id)

    # Projects
    projects: list[ProjectRead] = []
    if project_ids:
        result = await db.execute(
            select(Project).where(Project.project_id.in_(project_ids))
        )
        projects = [ProjectRead.model_validate(p) for p in result.scalars().all()]

    # Documents
    result = await db.execute(
        select(Document).where(Document.top_level_bucket == record_id)
    )
    docs = result.scalars().all()
    documents = [DocumentRead.model_validate(d) for d in docs]

    # Category counts
    cat_counts: dict[str, int] = defaultdict(int)
    dup_count = 0
    for d in docs:
        cat_counts[d.document_type_label or "Unknown"] += 1
        if d.is_content_duplicate:
            dup_count += 1

    # Personnel via project roles
    personnel_ids: set[str] = set()
    if project_ids:
        result = await db.execute(
            select(ProjectRole.personnel_id)
            .where(ProjectRole.project_id.in_(project_ids))
            .distinct()
        )
        personnel_ids = {r[0] for r in result.all() if r[0]}

    personnel: list[PersonnelRead] = []
    if personnel_ids:
        result = await db.execute(
            select(Personnel).where(Personnel.personnel_id.in_(personnel_ids))
        )
        personnel = [PersonnelRead.model_validate(p) for p in result.scalars().all()]

    return PilotRecordDetail(
        record_id=record_id,
        description=config["description"],
        awards=awards,
        proposals=proposals,
        projects=projects,
        documents=documents,
        personnel=personnel,
        document_count=len(documents),
        duplicate_count=dup_count,
        category_counts=dict(cat_counts),
    )


async def get_documents_filtered(
    db: AsyncSession,
    record_id: str | None = None,
    category: str | None = None,
    parent_type: str | None = None,
    is_duplicate: bool | None = None,
    search: str | None = None,
    page: int = 1,
    page_size: int = 25,
) -> DocumentFilterResult:
    """Paginated, filtered document query."""
    query = select(Document)
    count_query = select(func.count()).select_from(Document)

    filters = []
    if record_id:
        filters.append(Document.top_level_bucket == record_id)
    if category:
        filters.append(Document.document_type_label == category)
    if parent_type:
        filters.append(Document.parent_entity_type == parent_type)
    if is_duplicate is not None:
        filters.append(Document.is_content_duplicate == is_duplicate)
    if search:
        filters.append(Document.filename.ilike(f"%{search}%"))

    for f in filters:
        query = query.where(f)
        count_query = count_query.where(f)

    # Total count
    total = (await db.execute(count_query)).scalar() or 0

    # Paginated results
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size).order_by(Document.filename)
    result = await db.execute(query)
    items = [DocumentRead.model_validate(d) for d in result.scalars().all()]

    # Category facet counts (for the current filter minus category)
    facet_query = select(
        Document.document_type_label, func.count()
    ).group_by(Document.document_type_label)
    for f in filters:
        if "document_type_label" not in str(f):
            facet_query = facet_query.where(f)
    facet_result = await db.execute(facet_query)
    category_counts = {r[0] or "Unknown": r[1] for r in facet_result.all()}

    return DocumentFilterResult(
        items=items,
        total_count=total,
        page=page,
        page_size=page_size,
        category_counts=category_counts,
    )
