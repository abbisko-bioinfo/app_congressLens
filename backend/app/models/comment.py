from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.presentation import Presentation


class Comment(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "comments"

    presentation_id: Mapped[str] = mapped_column(ForeignKey("presentations.id", ondelete="CASCADE"), nullable=False)
    author: Mapped[str | None] = mapped_column(String(255), nullable=True)
    body: Mapped[str] = mapped_column(Text, nullable=False)

    presentation: Mapped["Presentation"] = relationship(back_populates="comments")