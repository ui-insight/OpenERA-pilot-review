"""Organization model — sponsors, departments, subrecipients."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Organization(Base):
    __tablename__ = "organizations"

    organization_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    organization_name: Mapped[str | None] = mapped_column(String(300))
    organization_type: Mapped[str | None] = mapped_column(String(50))
    source_value: Mapped[str | None] = mapped_column(String(300))
    source_system: Mapped[str | None] = mapped_column(String(100))
    parent_organization_id: Mapped[str | None] = mapped_column(String(80))
    needs_lookup: Mapped[bool] = mapped_column(default=False)
