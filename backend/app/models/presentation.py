import uuid
from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, CheckConstraint, DateTime, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.conference import Conference
    from app.models.session import Session
    from app.models.presentation_author import PresentationAuthor
    from app.models.attachment import Attachment
    from app.models.comment import Comment
    from app.models.annotation import Annotation
    from app.models.topic import Topic


class Presentation(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "presentations"
    __table_args__ = (
        Index("ix_presentations_conference_id", "conference_id"),
        Index("ix_presentations_session_id", "session_id"),
        Index("ix_presentations_source_presentation_id", "source_presentation_id"),
        Index("ix_presentations_source_content_id", "source_content_id"),
        Index("ix_presentations_presentation_number", "presentation_number"),
        Index("ix_presentations_abstract_number", "abstract_number"),
        Index("ix_presentations_doi", "doi"),
        Index("ix_presentations_clinical_trial_registry_number", "clinical_trial_registry_number"),
        Index("ix_presentations_start_time", "start_time"),
        Index("ix_presentations_summary_status", "summary_status"),
        CheckConstraint(
            "summary_status IN ('none', 'pending', 'processing', 'ready', 'failed')",
            name="ck_presentations_summary_status",
        ),
    )

    conference_id: Mapped[uuid.UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("conferences.id", ondelete="CASCADE"), nullable=False)
    session_id: Mapped[uuid.UUID | None] = mapped_column(PGUUID(as_uuid=True), ForeignKey("sessions.id", ondelete="SET NULL"), nullable=True)
    source_presentation_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_content_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    abstract_text: Mapped[str | None] = mapped_column(Text, nullable=True)
    abstract_html: Mapped[str | None] = mapped_column(Text, nullable=True)
    presentation_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    abstract_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    poster_board_number: Mapped[str | None] = mapped_column(String(100), nullable=True)
    presentation_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    activity: Mapped[str | None] = mapped_column(String(100), nullable=True)
    status: Mapped[str | None] = mapped_column(String(50), nullable=True)
    position_in_session: Mapped[int | None] = mapped_column(Integer, nullable=True)
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    timezone: Mapped[str | None] = mapped_column(String(100), nullable=True)
    presenter_name: Mapped[str | None] = mapped_column(String(500), nullable=True)
    first_author_name: Mapped[str | None] = mapped_column(String(500), nullable=True)
    author_block_html: Mapped[str | None] = mapped_column(Text, nullable=True)
    institution_block: Mapped[str | None] = mapped_column(Text, nullable=True)
    disclosure_block_html: Mapped[str | None] = mapped_column(Text, nullable=True)
    funding_sources: Mapped[list[str] | None] = mapped_column(ARRAY(Text), nullable=True)
    additional_funding_source: Mapped[str | None] = mapped_column(Text, nullable=True)
    doi: Mapped[str | None] = mapped_column(String(500), nullable=True)
    journal_citation: Mapped[str | None] = mapped_column(Text, nullable=True)
    clinical_trial_registry_number: Mapped[str | None] = mapped_column(String(255), nullable=True)
    source_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    disclosure_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    has_abstract: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    has_slides: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    has_posters: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    has_videos: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")
    summary_status: Mapped[str] = mapped_column(String(20), default="none", server_default="none")

    conference: Mapped["Conference"] = relationship(back_populates="presentations")
    session: Mapped["Session"] = relationship(back_populates="presentations")
    authors: Mapped[list["PresentationAuthor"]] = relationship(
        back_populates="presentation", lazy="selectin", order_by="PresentationAuthor.author_order"
    )
    attachments: Mapped[list["Attachment"]] = relationship(back_populates="presentation", lazy="selectin")
    comments: Mapped[list["Comment"]] = relationship(back_populates="presentation", lazy="selectin")
    annotations: Mapped[list["Annotation"]] = relationship(back_populates="presentation", lazy="selectin")
    topics: Mapped[list["Topic"]] = relationship(
        secondary="presentation_topics",
        back_populates="presentations",
        lazy="selectin",
    )