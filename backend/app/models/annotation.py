from typing import TYPE_CHECKING

import uuid

from sqlalchemy import ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.presentation import Presentation
    from app.models.attachment import Attachment


class Annotation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "annotations"
    __table_args__ = (
        Index("ix_annotations_presentation_id", "presentation_id"),
        Index("ix_annotations_attachment_id", "attachment_id"),
        Index("ix_annotations_created_at", "created_at"),
    )

    presentation_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("presentations.id", ondelete="CASCADE"), nullable=False)
    attachment_id: Mapped[uuid.UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("attachments.id", ondelete="SET NULL"), nullable=True)
    selected_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    note: Mapped[str] = mapped_column(Text, nullable=False)
    color: Mapped[str | None] = mapped_column(String(50), nullable=True)
    page_number: Mapped[int | None] = mapped_column(Integer, nullable=True)
    anchor_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    created_by: Mapped[str | None] = mapped_column(String(255), nullable=True)

    presentation: Mapped["Presentation"] = relationship(back_populates="annotations")
    attachment: Mapped["Attachment"] = relationship(lazy="selectin")