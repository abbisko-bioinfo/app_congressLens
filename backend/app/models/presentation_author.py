from typing import TYPE_CHECKING

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.presentation import Presentation


class PresentationAuthor(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "presentation_authors"

    presentation_id: Mapped[str] = mapped_column(ForeignKey("presentations.id", ondelete="CASCADE"), nullable=False)
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