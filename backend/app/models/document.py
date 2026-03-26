"""Document model — files linked to awards or proposals."""

from __future__ import annotations

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Document(Base):
    __tablename__ = "documents"

    document_id: Mapped[str] = mapped_column(String(80), primary_key=True)
    document_type_code: Mapped[str | None] = mapped_column(String(40))
    document_type_label: Mapped[str | None] = mapped_column(String(100))
    parent_entity_type: Mapped[str | None] = mapped_column(String(20))
    parent_entity_id: Mapped[str | None] = mapped_column(String(80))
    linked_proposal_id: Mapped[str | None] = mapped_column(String(80))
    top_level_bucket: Mapped[str | None] = mapped_column(String(40), index=True)
    filename: Mapped[str | None] = mapped_column(String(500))
    extension: Mapped[str | None] = mapped_column(String(20))
    mime_type: Mapped[str | None] = mapped_column(String(100))
    file_size_bytes: Mapped[int | None] = mapped_column(BigInteger)
    sha256: Mapped[str | None] = mapped_column(String(64))
    storage_relative_path: Mapped[str | None] = mapped_column(String(600))
    source_system: Mapped[str | None] = mapped_column(String(100))
    is_content_duplicate: Mapped[bool] = mapped_column(default=False)
    needs_review: Mapped[str | None] = mapped_column(String(100))
