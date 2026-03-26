"""Award model — funded awards from sponsors."""

from __future__ import annotations

import datetime

from sqlalchemy import Date, Float, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Award(Base):
    __tablename__ = "awards"

    award_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    award_number: Mapped[str | None] = mapped_column(String(80))
    award_title: Mapped[str | None] = mapped_column(String(500))
    proposal_id: Mapped[str | None] = mapped_column(String(80))
    project_id: Mapped[str | None] = mapped_column(String(80))
    sponsor_organization_id: Mapped[str | None] = mapped_column(String(80))
    award_status: Mapped[str | None] = mapped_column(String(30))
    original_start_date: Mapped[datetime.date | None] = mapped_column(Date)
    current_end_date: Mapped[datetime.date | None] = mapped_column(Date)
    adjusted_budget: Mapped[float | None] = mapped_column(Float)
    cumulative_funding_amount: Mapped[float | None] = mapped_column(Float)
    source_system: Mapped[str | None] = mapped_column(String(100))
    needs_veras_title: Mapped[bool] = mapped_column(default=False)
    title_source_path: Mapped[str | None] = mapped_column(String(500))
    title_source_type: Mapped[str | None] = mapped_column(String(60))
