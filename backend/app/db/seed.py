"""Seed the database from staging CSV files."""

from __future__ import annotations

import csv
import datetime
import logging
from pathlib import Path

from sqlalchemy import select, text

from app.db.engine import async_session
from app.models.allowed_value import AllowedValue
from app.models.award import Award
from app.models.document import Document
from app.models.organization import Organization
from app.models.personnel import Personnel
from app.models.project import Project
from app.models.project_role import ProjectRole
from app.models.proposal import Proposal

logger = logging.getLogger(__name__)

SEED_DIR = Path(__file__).resolve().parents[2] / "seed_data"


def _bool(val: str) -> bool:
    return val.strip().upper() in ("Y", "YES", "TRUE", "1")


def _date(val: str) -> datetime.date | None:
    val = val.strip()
    if not val:
        return None
    try:
        return datetime.date.fromisoformat(val)
    except ValueError:
        return None


def _float(val: str) -> float | None:
    val = val.strip()
    if not val:
        return None
    try:
        return float(val)
    except ValueError:
        return None


def _int(val: str) -> int | None:
    val = val.strip()
    if not val:
        return None
    try:
        return int(val)
    except ValueError:
        return None


def _str(val: str) -> str | None:
    val = val.strip()
    return val if val else None


def _read_csv(filename: str) -> list[dict]:
    path = SEED_DIR / filename
    if not path.exists():
        logger.warning("Seed file not found: %s", path)
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


async def seed_db() -> None:
    """Load seed data from CSVs into the database.

    Skips seeding if the database already contains data.
    """
    async with async_session() as session:
        # Check if already seeded
        result = await session.execute(
            select(Award.award_id).limit(1)
        )
        if result.first() is not None:
            logger.info("Database already seeded — skipping.")
            return

        logger.info("Seeding database from %s ...", SEED_DIR)

        # 1. AllowedValues
        rows = _read_csv("allowed_values_document_types.csv")
        for r in rows:
            session.add(AllowedValue(
                allowed_value_id=r["allowed_value_id"],
                group_name=_str(r["group_name"]),
                code=_str(r["code"]),
                label=_str(r["label"]),
                description=_str(r.get("description", "")),
            ))
        await session.flush()
        logger.info("  AllowedValues: %d rows", len(rows))

        # 2. Organizations
        rows = _read_csv("organizations.csv")
        for r in rows:
            session.add(Organization(
                organization_id=r["organization_id"],
                organization_name=_str(r.get("organization_name", "")),
                organization_type=_str(r.get("organization_type", "")),
                source_value=_str(r.get("source_value", "")),
                source_system=_str(r.get("source_system", "")),
                parent_organization_id=_str(r.get("parent_organization_id", "")),
                needs_lookup=_bool(r.get("needs_lookup", "")),
            ))
        await session.flush()
        logger.info("  Organizations: %d rows", len(rows))

        # 3. Personnel
        rows = _read_csv("personnel.csv")
        for r in rows:
            session.add(Personnel(
                personnel_id=r["personnel_id"],
                full_name=_str(r.get("full_name", "")),
                last_name=_str(r.get("last_name", "")),
                first_name=_str(r.get("first_name", "")),
                person_type=_str(r.get("person_type", "")),
                department_organization_id=_str(r.get("department_organization_id", "")),
                source_system=_str(r.get("source_system", "")),
                institutional_id_candidate=_str(r.get("institutional_id_candidate", "")),
                needs_identity_review=_bool(r.get("needs_identity_review", "")),
            ))
        await session.flush()
        logger.info("  Personnel: %d rows", len(rows))

        # 4. Projects
        rows = _read_csv("projects.csv")
        for r in rows:
            session.add(Project(
                project_id=r["project_id"],
                project_title=_str(r.get("project_title", "")),
                project_status=_str(r.get("project_status", "")),
                lead_organization_id=_str(r.get("lead_organization_id", "")),
                sponsor_organization_id=_str(r.get("sponsor_organization_id", "")),
                start_date=_date(r.get("start_date", "")),
                end_date=_date(r.get("end_date", "")),
                source_proposal_number=_str(r.get("source_proposal_number", "")),
                needs_veras_title=_bool(r.get("needs_veras_title", "")),
                title_source_type=_str(r.get("title_source_type", "")),
            ))
        await session.flush()
        logger.info("  Projects: %d rows", len(rows))

        # 5. Proposals
        rows = _read_csv("proposals.csv")
        for r in rows:
            session.add(Proposal(
                proposal_id=r["proposal_id"],
                proposal_number=_str(r.get("proposal_number", "")),
                proposal_title=_str(r.get("proposal_title", "")),
                project_id=_str(r.get("project_id", "")),
                sponsor_organization_id=_str(r.get("sponsor_organization_id", "")),
                lead_organization_id=_str(r.get("lead_organization_id", "")),
                proposal_status=_str(r.get("proposal_status", "")),
                start_date=_date(r.get("start_date", "")),
                end_date=_date(r.get("end_date", "")),
                source_system=_str(r.get("source_system", "")),
                needs_veras_enrichment=_bool(r.get("needs_veras_enrichment", "")),
                title_source_path=_str(r.get("title_source_path", "")),
                title_source_type=_str(r.get("title_source_type", "")),
            ))
        await session.flush()
        logger.info("  Proposals: %d rows", len(rows))

        # 6. Awards
        rows = _read_csv("awards.csv")
        for r in rows:
            session.add(Award(
                award_id=r["award_id"],
                award_number=_str(r.get("award_number", "")),
                award_title=_str(r.get("award_title", "")),
                proposal_id=_str(r.get("proposal_id", "")),
                project_id=_str(r.get("project_id", "")),
                sponsor_organization_id=_str(r.get("sponsor_organization_id", "")),
                award_status=_str(r.get("award_status", "")),
                original_start_date=_date(r.get("original_start_date", "")),
                current_end_date=_date(r.get("current_end_date", "")),
                adjusted_budget=_float(r.get("adjusted_budget", "")),
                cumulative_funding_amount=_float(r.get("cumulative_funding_amount", "")),
                source_system=_str(r.get("source_system", "")),
                needs_veras_title=_bool(r.get("needs_veras_title", "")),
                title_source_path=_str(r.get("title_source_path", "")),
                title_source_type=_str(r.get("title_source_type", "")),
            ))
        await session.flush()
        logger.info("  Awards: %d rows", len(rows))

        # 7. Documents
        rows = _read_csv("documents.csv")
        for r in rows:
            session.add(Document(
                document_id=r["document_id"],
                document_type_code=_str(r.get("document_type_code", "")),
                document_type_label=_str(r.get("document_type_label", "")),
                parent_entity_type=_str(r.get("parent_entity_type", "")),
                parent_entity_id=_str(r.get("parent_entity_id", "")),
                linked_proposal_id=_str(r.get("linked_proposal_id", "")),
                top_level_bucket=_str(r.get("top_level_bucket", "")),
                filename=_str(r.get("filename", "")),
                extension=_str(r.get("extension", "")),
                mime_type=_str(r.get("mime_type", "")),
                file_size_bytes=_int(r.get("file_size_bytes", "")),
                sha256=_str(r.get("sha256", "")),
                storage_relative_path=_str(r.get("storage_relative_path", "")),
                source_system=_str(r.get("source_system", "")),
                is_content_duplicate=_bool(r.get("is_content_duplicate", "")),
                needs_review=_str(r.get("needs_review", "")),
            ))
        await session.flush()
        logger.info("  Documents: %d rows", len(rows))

        # 8. ProjectRoles
        rows = _read_csv("project_roles.csv")
        for r in rows:
            session.add(ProjectRole(
                project_role_id=r["project_role_id"],
                project_id=_str(r.get("project_id", "")),
                personnel_id=_str(r.get("personnel_id", "")),
                role_code=_str(r.get("role_code", "")),
                key_personnel=_bool(r.get("key_personnel", "")),
                funding_award_id=_str(r.get("funding_award_id", "")),
                source_system=_str(r.get("source_system", "")),
            ))
        await session.flush()
        logger.info("  ProjectRoles: %d rows", len(rows))

        await session.commit()
        logger.info("Seeding complete.")
