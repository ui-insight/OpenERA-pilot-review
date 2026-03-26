"""Proposal model — grant proposals submitted to sponsors."""

from __future__ import annotations

import datetime

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Proposal(Base):
    __tablename__ = "proposals"

    proposal_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    proposal_number: Mapped[str | None] = mapped_column(String(80))
    proposal_title: Mapped[str | None] = mapped_column(String(500))
    project_id: Mapped[str | None] = mapped_column(String(80))
    sponsor_organization_id: Mapped[str | None] = mapped_column(String(80))
    lead_organization_id: Mapped[str | None] = mapped_column(String(80))
    proposal_status: Mapped[str | None] = mapped_column(String(30))
    start_date: Mapped[datetime.date | None] = mapped_column(Date)
    end_date: Mapped[datetime.date | None] = mapped_column(Date)
    source_system: Mapped[str | None] = mapped_column(String(100))
    needs_veras_enrichment: Mapped[bool] = mapped_column(default=False)
    title_source_path: Mapped[str | None] = mapped_column(String(500))
    title_source_type: Mapped[str | None] = mapped_column(String(60))
