from typing import TYPE_CHECKING

import uuid

from sqlalchemy import Boolean, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.presentation import Presentation


class PresentationAuthor(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "presentation_authors"
    __table_args__ = (
        Index("ix_presentation_authors_presentation_id", "presentation_id"),
        Index("ix_presentation_authors_normalized_name", "normalized_name"),
        Index("ix_presentation_authors_organization", "organization"),
        Index("ix_presentation_authors_author_order", "author_order"),
        Index("ix_presentation_authors_is_first_author", "is_first_author"),
        Index("ix_presentation_authors_is_presenter", "is_presenter"),
    )

    presentation_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("presentations.id", ondelete="CASCADE"), nullable=False)
    source_author_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    display_name: Mapped[str] = mapped_column(String(500), nullable=False)
    normalized_name: Mapped[str | None] = mapped_column(String(500), nullable=True)
    role: Mapped[str | None] = mapped_column(String(100), nullable=True)
    author_order: Mapped[int | None] = mapped_column(Integer, nullable=True)
    organization: Mapped[str | None] = mapped_column(Text, nullable=True)
    city: Mapped[str | None] = mapped_column(String(255), nullable=True)
    country: Mapped[str | None] = mapped_column(String(100), nullable=True)
    picture_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_first_author: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    is_presenter: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")

    presentation: Mapped["Presentation"] = relationship(back_populates="authors")