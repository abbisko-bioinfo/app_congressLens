from sqlalchemy import CheckConstraint, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import TYPE_CHECKING

from app.models.base import Base, UUIDMixin, TimestampMixin

if TYPE_CHECKING:
    from app.models.presentation import Presentation


class Topic(Base, UUIDMixin, TimestampMixin):
    __tablename__ = "topics"
    __table_args__ = (
        UniqueConstraint("normalized_name", "type", name="uq_topic_normalized_name_type"),
        CheckConstraint("type IN ('topic', 'keyword', 'track', 'subtrack')", name="ck_topics_type"),
    )

    name: Mapped[str] = mapped_column(String(500), nullable=False)
    normalized_name: Mapped[str] = mapped_column(String(500), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)

    presentations: Mapped[list["Presentation"]] = relationship(
        secondary="presentation_topics",
        back_populates="topics",
        lazy="selectin",
    )