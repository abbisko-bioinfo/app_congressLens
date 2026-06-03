from typing import TYPE_CHECKING

import uuid

from sqlalchemy import ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.presentation import Presentation


class Comment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "comments"
    __table_args__ = (
        Index("ix_comments_presentation_id", "presentation_id"),
        Index("ix_comments_created_at", "created_at"),
    )

    presentation_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("presentations.id", ondelete="CASCADE"), nullable=False)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    presentation: Mapped["Presentation"] = relationship(back_populates="comments")