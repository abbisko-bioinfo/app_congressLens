from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BigInteger, DateTime, ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, UUIDMixin

if TYPE_CHECKING:
    from app.models.presentation import Presentation


class Attachment(Base, UUIDMixin):
    __tablename__ = "attachments"

    presentation_id: Mapped[str] = mapped_column(ForeignKey("presentations.id", ondelete="CASCADE"), nullable=False)
    original_filename: Mapped[str] = mapped_column(Text, nullable=False)
    original_object_key: Mapped[str] = mapped_column(Text, nullable=False)
    bucket_name: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    file_size: Mapped[int | None] = mapped_column(BigInteger, nullable=True)
    preview_object_key: Mapped[str | None] = mapped_column(Text, nullable=True)
    preview_content_type: Mapped[str | None] = mapped_column(String(255), nullable=True)
    preview_status: Mapped[str] = mapped_column(String(20), default="pending", server_default="pending")
    conversion_error: Mapped[str | None] = mapped_column(Text, nullable=True)
    uploaded_by: Mapped[str | None] = mapped_column(String(255), nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default="now()")

    presentation: Mapped["Presentation"] = relationship(back_populates="attachments")