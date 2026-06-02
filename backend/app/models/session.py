from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.conference import Conference
    from app.models.presentation import Presentation


class Session(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "sessions"

    conference_id: Mapped[str] = mapped_column(ForeignKey("conferences.id", ondelete="CASCADE"), nullable=False)
    source_session_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    session_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    track: Mapped[str | None] = mapped_column(String(255), nullable=True)
    subtrack: Mapped[str | None] = mapped_column(String(255), nullable=True)
    room: Mapped[str | None] = mapped_column(String(255), nullable=True)
    start_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    end_time: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    timezone: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    is_on_demand: Mapped[bool] = mapped_column(Boolean, default=False, server_default="false")

    conference: Mapped["Conference"] = relationship(back_populates="sessions")
    presentations: Mapped[list["Presentation"]] = relationship(back_populates="session", lazy="selectin")