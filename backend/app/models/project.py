"""Project model — research initiatives linked to proposals and awards."""

from __future__ import annotations

import datetime

from sqlalchemy import Date, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Project(Base):
    __tablename__ = "projects"

    project_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    project_title: Mapped[str | None] = mapped_column(String(500))
    project_status: Mapped[str | None] = mapped_column(String(30))
    lead_organization_id: Mapped[str | None] = mapped_column(String(80))
    sponsor_organization_id: Mapped[str | None] = mapped_column(String(80))
    start_date: Mapped[datetime.date | None] = mapped_column(Date)
    end_date: Mapped[datetime.date | None] = mapped_column(Date)
    source_proposal_number: Mapped[str | None] = mapped_column(String(80))
    needs_veras_title: Mapped[bool] = mapped_column(default=False)
    title_source_type: Mapped[str | None] = mapped_column(String(60))
