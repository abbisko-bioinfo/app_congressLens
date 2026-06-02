from datetime import date
from typing import TYPE_CHECKING

from sqlalchemy import Integer, String, Text, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.session import Session
    from app.models.presentation import Presentation


class Conference(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "conferences"
    __table_args__ = (UniqueConstraint("acronym", "year", name="uq_conference_acronym_year"),)

    acronym: Mapped[str] = mapped_column(String(50), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    location: Mapped[str | None] = mapped_column(Text, nullable=True)
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    timezone: Mapped[str | None] = mapped_column(String(100), nullable=True)
    website: Mapped[str | None] = mapped_column(Text, nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    sessions: Mapped[list["Session"]] = relationship(back_populates="conference", lazy="selectin")
    presentations: Mapped[list["Presentation"]] = relationship(back_populates="conference", lazy="selectin")