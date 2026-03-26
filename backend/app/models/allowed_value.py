"""AllowedValue model — lookup values for document types and other taxonomies."""

from __future__ import annotations

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class AllowedValue(Base):
    __tablename__ = "allowed_values"

    allowed_value_id: Mapped[str] = mapped_column(String(40), primary_key=True)
    group_name: Mapped[str | None] = mapped_column(String(60))
    code: Mapped[str | None] = mapped_column(String(40))
    label: Mapped[str | None] = mapped_column(String(100))
    description: Mapped[str | None] = mapped_column(String(300))
