"""Personnel model — PIs, co-PIs, and other research staff."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Personnel(Base):
    __tablename__ = "personnel"

    personnel_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    full_name: Mapped[str | None] = mapped_column(String(200))
    last_name: Mapped[str | None] = mapped_column(String(100))
    first_name: Mapped[str | None] = mapped_column(String(100))
    person_type: Mapped[str | None] = mapped_column(String(60))
    department_organization_id: Mapped[str | None] = mapped_column(String(80))
    source_system: Mapped[str | None] = mapped_column(String(100))
    institutional_id_candidate: Mapped[str | None] = mapped_column(String(80))
    needs_identity_review: Mapped[bool] = mapped_column(default=False)
