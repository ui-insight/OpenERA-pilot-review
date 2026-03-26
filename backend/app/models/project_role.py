"""ProjectRole model — role assignments linking personnel to projects."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ProjectRole(Base):
    __tablename__ = "project_roles"

    project_role_id: Mapped[str] = mapped_column(String(160), primary_key=True)
    project_id: Mapped[str | None] = mapped_column(String(80))
    personnel_id: Mapped[str | None] = mapped_column(String(80))
    role_code: Mapped[str | None] = mapped_column(String(30))
    key_personnel: Mapped[bool] = mapped_column(default=False)
    funding_award_id: Mapped[str | None] = mapped_column(String(80))
    source_system: Mapped[str | None] = mapped_column(String(100))
